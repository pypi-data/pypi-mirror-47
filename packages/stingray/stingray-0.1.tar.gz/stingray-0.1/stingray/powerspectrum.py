from __future__ import division
import numpy as np
import scipy
import scipy.stats
import scipy.fftpack
import scipy.optimize
import logging

import stingray.lightcurve as lightcurve
import stingray.utils as utils
from stingray.gti import bin_intervals_from_gtis, check_gtis
from stingray.utils import simon
from stingray.crossspectrum import Crossspectrum, AveragedCrossspectrum

__all__ = ["Powerspectrum", "AveragedPowerspectrum", "DynamicalPowerspectrum"]


def classical_pvalue(power, nspec):
    """
    Compute the probability of detecting the current power under
    the assumption that there is no periodic oscillation in the data.

    This computes the single-trial p-value that the power was
    observed under the null hypothesis that there is no signal in
    the data.

    Important: the underlying assumptions that make this calculation valid
    are:

    1. the powers in the power spectrum follow a chi-square distribution
    2. the power spectrum is normalized according to [Leahy 1983]_, such
       that the powers have a mean of 2 and a variance of 4
    3. there is only white noise in the light curve. That is, there is no
       aperiodic variability that would change the overall shape of the power
       spectrum.

    Also note that the p-value is for a *single trial*, i.e. the power
    currently being tested. If more than one power or more than one power
    spectrum are being tested, the resulting p-value must be corrected for the
    number of trials (Bonferroni correction).

    Mathematical formulation in [Groth 1975]_.
    Original implementation in IDL by Anna L. Watts.

    Parameters
    ----------
    power :  float
        The squared Fourier amplitude of a spectrum to be evaluated

    nspec : int
        The number of spectra or frequency bins averaged in ``power``.
        This matters because averaging spectra or frequency bins increases
        the signal-to-noise ratio, i.e. makes the statistical distributions
        of the noise narrower, such that a smaller power might be very
        significant in averaged spectra even though it would not be in a single
        power spectrum.

    Returns
    -------
    pval : float
        The classical p-value of the observed power being consistent with
        the null hypothesis of white noise

    References
    ----------

    * .. [Leahy 1983] https://ui.adsabs.harvard.edu/#abs/1983ApJ...266..160L/abstract
    * .. [Groth 1975] https://ui.adsabs.harvard.edu/#abs/1975ApJS...29..285G/abstract

    """
    if not np.isfinite(power):
        raise ValueError("power must be a finite floating point number!")

    if power < 0:
        raise ValueError("power must be a positive real number!")

    if not np.isfinite(nspec):
        raise ValueError("nspec must be a finite integer number")

    if nspec < 1:
        raise ValueError("nspec must be larger or equal to 1")

    if not np.isclose(nspec % 1, 0):
        raise ValueError("nspec must be an integer number!")

    # If the power is really big, it's safe to say it's significant,
    # and the p-value will be nearly zero
    if (power * nspec) > 30000:
        simon("Probability of no signal too miniscule to calculate.")
        return 0.0

    else:
        pval = _pavnosigfun(power, nspec)
        return pval


def _pavnosigfun(power, nspec):
    """
    Helper function doing the actual calculation of the p-value.

    Parameters
    ----------
    power : float
        The measured candidate power

    nspec : int
        The number of power spectral bins that were averaged in `power`
        (note: can be either through averaging spectra or neighbouring bins)
    """
    sum = 0.0
    m = nspec - 1

    pn = power * nspec

    while m >= 0:

        s = 0.0
        for i in range(int(m) - 1):
            s += np.log(float(m - i))

        logterm = m * np.log(pn / 2) - pn / 2 - s
        term = np.exp(logterm)
        ratio = sum / term

        if ratio > 1.0e15:
            return sum

        sum += term
        m -= 1

    return sum


class Powerspectrum(Crossspectrum):
    """
    Make a :class:`Powerspectrum` (also called periodogram) from a (binned) light curve.
    Periodograms can be normalized by either Leahy normalization, fractional rms
    normalizaation, absolute rms normalization, or not at all.

    You can also make an empty :class:`Powerspectrum` object to populate with your
    own fourier-transformed data (this can sometimes be useful when making
    binned power spectra).

    Parameters
    ----------
    lc: :class:`stingray.Lightcurve` object, optional, default ``None``
        The light curve data to be Fourier-transformed.

    norm: {``leahy`` | ``frac`` | ``abs`` | ``none`` }, optional, default ``frac``
        The normaliation of the power spectrum to be used. Options are
        ``leahy``, ``frac``, ``abs`` and ``none``, default is ``frac``.

    Other Parameters
    ----------------
    gti: 2-d float array
        ``[[gti0_0, gti0_1], [gti1_0, gti1_1], ...]`` -- Good Time intervals.
        This choice overrides the GTIs in the single light curves. Use with
        care!

    Attributes
    ----------
    norm: {``leahy`` | ``frac`` | ``abs`` | ``none`` }
        the normalization of the power spectrun

    freq: numpy.ndarray
        The array of mid-bin frequencies that the Fourier transform samples

    power: numpy.ndarray
        The array of normalized squared absolute values of Fourier
        amplitudes

    power_err: numpy.ndarray
        The uncertainties of ``power``.
        An approximation for each bin given by ``power_err= power/sqrt(m)``.
        Where ``m`` is the number of power averaged in each bin (by frequency
        binning, or averaging power spectrum). Note that for a single
        realization (``m=1``) the error is equal to the power.

    df: float
        The frequency resolution

    m: int
        The number of averaged powers in each bin

    n: int
        The number of data points in the light curve

    nphots: float
        The total number of photons in the light curve

    """
    def __init__(self, lc=None, norm='frac', gti=None):
        Crossspectrum.__init__(self, lc1=lc, lc2=lc, norm=norm, gti=gti)
        self.nphots = self.nphots1

    def rebin(self, df=None, f=None, method="mean"):
        """
        Rebin the power spectrum.

        Parameters
        ----------
        df: float
            The new frequency resolution

        Other Parameters
        ----------------
        f: float
            the rebin factor. If specified, it substitutes ``df`` with ``f*self.df``

        Returns
        -------
        bin_cs = :class:`Powerspectrum` object
            The newly binned power spectrum.
        """
        bin_ps = Crossspectrum.rebin(self, df=df, f=f, method=method)
        bin_ps.nphots = bin_ps.nphots1

        return bin_ps

    def compute_rms(self, min_freq, max_freq, white_noise_offset=0.):
        """
        Compute the fractional rms amplitude in the power spectrum
        between two frequencies.

        Parameters
        ----------
        min_freq: float
            The lower frequency bound for the calculation

        max_freq: float
            The upper frequency bound for the calculation

        Other parameters
        ----------------
        white_noise_offset : float, default 0
            This is the white noise level, in Leahy normalization. In the ideal
            case, this is 2. Dead time and other instrumental effects can alter
            it. The user can fit the white noise level outside this function
            and it will get subtracted from powers here.

        Returns
        -------
        rms: float
            The fractional rms amplitude contained between ``min_freq`` and
            ``max_freq``

        """
        minind = self.freq.searchsorted(min_freq)
        maxind = self.freq.searchsorted(max_freq)
        powers = self.power[minind:maxind]
        nphots = self.nphots

        if self.norm.lower() == 'leahy':
            powers_leahy = powers.copy()
        elif self.norm.lower() == "frac":
            powers_leahy = \
                self.unnorm_power[minind:maxind].real * 2 / nphots
        else:
            raise TypeError("Normalization not recognized!")

        rms = np.sqrt(np.sum(powers_leahy - white_noise_offset) / nphots)
        rms_err = self._rms_error(powers_leahy)

        return rms, rms_err

    def _rms_error(self, powers):
        """
        Compute the error on the fractional rms amplitude using error
        propagation.
        Note: this uses the actual measured powers, which is not
        strictly correct. We should be using the underlying power spectrum,
        but in the absence of an estimate of that, this will have to do.

        .. math::

           r = \sqrt{P}

        .. math::

           \delta r = \\frac{1}{2 * \sqrt{P}} \delta P

        Parameters
        ----------
        powers: iterable
            The list of powers used to compute the fractional rms amplitude.

        Returns
        -------
        delta_rms: float
            the error on the fractional rms amplitude
        """
        nphots = self.nphots
        p_err = scipy.stats.chi2(2.0 * self.m).var() * powers / self.m / nphots

        rms = np.sum(powers) / nphots
        pow = np.sqrt(rms)

        drms_dp = 1 / (2 * pow)

        sq_sum_err = np.sqrt(np.sum(p_err**2))
        delta_rms = sq_sum_err * drms_dp
        return delta_rms

    def classical_significances(self, threshold=1, trial_correction=False):
        """
        Compute the classical significances for the powers in the power
        spectrum, assuming an underlying noise distribution that follows a
        chi-square distributions with 2M degrees of freedom, where M is the
        number of powers averaged in each bin.

        Note that this function will *only* produce correct results when the
        following underlying assumptions are fulfilled:

        1. The power spectrum is Leahy-normalized
        2. There is no source of variability in the data other than the
           periodic signal to be determined with this method. This is important!
           If there are other sources of (aperiodic) variability in the data, this
           method will *not* produce correct results, but instead produce a large
           number of spurious false positive detections!
        3. There are no significant instrumental effects changing the
           statistical distribution of the powers (e.g. pile-up or dead time)

        By default, the method produces ``(index,p-values)`` for all powers in
        the power spectrum, where index is the numerical index of the power in
        question. If a ``threshold`` is set, then only powers with p-values
        *below* that threshold with their respective indices. If
        ``trial_correction`` is set to ``True``, then the threshold will be corrected
        for the number of trials (frequencies) in the power spectrum before
        being used.

        Parameters
        ----------
        threshold : float, optional, default ``1``
            The threshold to be used when reporting p-values of potentially
            significant powers. Must be between 0 and 1.
            Default is ``1`` (all p-values will be reported).

        trial_correction : bool, optional, default ``False``
            A Boolean flag that sets whether the ``threshold`` will be corrected
            by the number of frequencies before being applied. This decreases
            the ``threshold`` (p-values need to be lower to count as significant).
            Default is ``False`` (report all powers) though for any application
            where `threshold`` is set to something meaningful, this should also
            be applied!

        Returns
        -------
        pvals : iterable
            A list of ``(index, p-value)`` tuples for all powers that have p-values
            lower than the threshold specified in ``threshold``.

        """
        if not self.norm == "leahy":
            raise ValueError("This method only works on "
                             "Leahy-normalized power spectra!")

        if np.size(self.m) == 1:
            # calculate p-values for all powers
            # leave out zeroth power since it just encodes the number of photons!
            pv = np.array([classical_pvalue(power, self.m)
                           for power in self.power])
        else:
            pv = np.array([classical_pvalue(power, m)
                           for power, m in zip(self.power, self.m)])

        # if trial correction is used, then correct the threshold for
        # the number of powers in the power spectrum
        if trial_correction:
            threshold /= self.power.shape[0]

        # need to add 1 to the indices to make up for the fact that
        # we left out the first power above!
        indices = np.where(pv < threshold)[0]

        pvals = np.vstack([pv[indices], indices])

        return pvals


class AveragedPowerspectrum(AveragedCrossspectrum, Powerspectrum):
    """
    Make an averaged periodogram from a light curve by segmenting the light
    curve, Fourier-transforming each segment and then averaging the
    resulting periodograms.

    Parameters
    ----------
    lc: :class:`stingray.Lightcurve`object OR iterable of :class:`stingray.Lightcurve` objects
        The light curve data to be Fourier-transformed.

    segment_size: float
        The size of each segment to average. Note that if the total
        duration of each :class:`Lightcurve` object in lc is not an integer multiple
        of the ``segment_size``, then any fraction left-over at the end of the
        time series will be lost.

    norm: {``leahy`` | ``frac`` | ``abs`` | ``none`` }, optional, default ``frac``
        The normaliation of the periodogram to be used.


    Other Parameters
    ----------------
    gti: 2-d float array
        ``[[gti0_0, gti0_1], [gti1_0, gti1_1], ...]`` -- Good Time intervals.
        This choice overrides the GTIs in the single light curves. Use with
        care!

    Attributes
    ----------
    norm: {``leahy`` | ``frac`` | ``abs`` | ``none`` }
        the normalization of the periodogram

    freq: numpy.ndarray
        The array of mid-bin frequencies that the Fourier transform samples

    power: numpy.ndarray
        The array of normalized squared absolute values of Fourier
        amplitudes

    power_err: numpy.ndarray
        The uncertainties of ``power``.
        An approximation for each bin given by ``power_err= power/sqrt(m)``.
        Where ``m`` is the number of power averaged in each bin (by frequency
        binning, or averaging powerspectrum). Note that for a single
        realization (``m=1``) the error is equal to the power.

    df: float
        The frequency resolution

    m: int
        The number of averaged periodograms

    n: int
        The number of data points in the light curve

    nphots: float
        The total number of photons in the light curve

    """
    def __init__(self, lc=None, segment_size=None, norm="frac", gti=None):

        self.type = "powerspectrum"

        if segment_size is None and lc is not None:
            raise ValueError("segment_size must be specified")
        if segment_size is not None and not np.isfinite(segment_size):
            raise ValueError("segment_size must be finite!")

        self.segment_size = segment_size

        Powerspectrum.__init__(self, lc, norm, gti=gti)

        return

    def _make_segment_spectrum(self, lc, segment_size):
        """
        Split the light curves into segments of size ``segment_size``, and calculate a power spectrum for
        each.

        Parameters
        ----------
        lc  : :class:`stingray.Lightcurve` objects\
            The input light curve

        segment_size : ``numpy.float``
            Size of each light curve segment to use for averaging.

        Returns
        -------
        power_all : list of :class:`Powerspectrum` objects
            A list of power spectra calculated independently from each light curve segment

        nphots_all : ``numpy.ndarray``
            List containing the number of photons for all segments calculated from ``lc``
        """
        if not isinstance(lc, lightcurve.Lightcurve):
            raise TypeError("lc must be a lightcurve.Lightcurve object")

        if self.gti is None:
            self.gti = lc.gti
        check_gtis(self.gti)

        start_inds, end_inds = \
            bin_intervals_from_gtis(self.gti, segment_size, lc.time, dt=lc.dt)

        power_all = []
        nphots_all = []
        for start_ind, end_ind in zip(start_inds, end_inds):
            time = lc.time[start_ind:end_ind]
            counts = lc.counts[start_ind:end_ind]
            counts_err = lc.counts_err[start_ind: end_ind]
            lc_seg = lightcurve.Lightcurve(time, counts, err=counts_err,
                                           err_dist=lc.err_dist.lower())
            power_seg = Powerspectrum(lc_seg, norm=self.norm)
            power_all.append(power_seg)
            nphots_all.append(np.sum(lc_seg.counts))

        return power_all, nphots_all


class DynamicalPowerspectrum(AveragedPowerspectrum):
    """
    Create a dynamical power spectrum, also often called a *spectrogram*.

    This class will divide a :class:`Lightcurve` object into segments of
    length ``segment_size``, create a power spectrum for each segment and store
    all powers in a matrix as a function of both time (using the mid-point of each
    segment) and frequency.

    This is often used to trace changes in period of a (quasi-)periodic signal over
    time.

    Parameters
    ----------
    lc : :class:`stingray.Lightcurve` object
        The time series of which the Dynamical powerspectrum is
        to be calculated.

    segment_size : float, default 1
         Length of the segment of light curve, default value is 1 (in whatever units
         the ``time`` array in the :class:`Lightcurve`` object uses).

    norm: {``leahy`` | ``frac`` | ``abs`` | ``none`` }, optional, default ``frac``
        The normaliation of the periodogram to be used.

    Other Parameters
    ----------------
    gti: 2-d float array
        ``[[gti0_0, gti0_1], [gti1_0, gti1_1], ...]`` -- Good Time intervals.
        This choice overrides the GTIs in the single light curves. Use with
        care!

    Attributes
    ----------
    segment_size: float
        The size of each segment to average. Note that if the total
        duration of each Lightcurve object in lc is not an integer multiple
        of the ``segment_size``, then any fraction left-over at the end of the
        time series will be lost.

    dyn_ps : np.ndarray
        The matrix of normalized squared absolute values of Fourier
        amplitudes. The axis are given by the ``freq``
        and ``time`` attributes

    norm: {``leahy`` | ``frac`` | ``abs`` | ``none``}
        the normalization of the periodogram

    freq: numpy.ndarray
        The array of mid-bin frequencies that the Fourier transform samples

    df: float
        The frequency resolution

    dt: float
        The time resolution
    """

    def __init__(self, lc, segment_size, norm="frac", gti=None):
        if segment_size < 2 * lc.dt:
            raise ValueError("Length of the segment is too short to form a "
                             "light curve!")
        elif segment_size > lc.tseg:
            raise ValueError("Length of the segment is too long to create "
                             "any segments of the light curve!")
        AveragedPowerspectrum.__init__(self, lc=lc,
                                       segment_size=segment_size, norm=norm,
                                       gti=gti)
        self._make_matrix(lc)

    def _make_matrix(self, lc):
        """
        Create a matrix of powers for each time step (rows) and each frequency step (columns).

        Parameters
        ----------
        lc : :class:`Lightcurve` object
            The :class:`Lightcurve` object from which to generate the dynamical power spectrum
        """
        ps_all, _ = AveragedPowerspectrum._make_segment_spectrum(
            self, lc, self.segment_size)
        self.dyn_ps = np.array([ps.power for ps in ps_all]).T

        self.freq = ps_all[0].freq

        start_inds, end_inds = \
            bin_intervals_from_gtis(self.gti, self.segment_size, lc.time, dt=lc.dt)


        tstart = lc.time[start_inds]
        tend = lc.time[end_inds]

        self.time = tstart + 0.5*(tend - tstart)

        # Assign length of lightcurve as time resolution if only one value
        if len(self.time) > 1:
            self.dt = self.time[1] - self.time[0]
        else:
            self.dt = lc.n

        # Assign biggest freq. resolution if only one value
        if len(self.freq) > 1:
            self.df = self.freq[1] - self.freq[0]
        else:
            self.df = 1 / lc.n

    def rebin_frequency(self, df_new, method="sum"):
        """
        Rebin the Dynamic Power Spectrum to a new frequency resolution. Rebinning is
        an in-place operation, i.e. will replace the existing ``dyn_ps`` attribute.

        While the new resolution need not be an integer multiple of the
        previous frequency resolution, be aware that if it is not, the last
        bin will be cut off by the fraction left over by the integer division.

        Parameters
        ----------
        df_new: float
            The new frequency resolution of the Dynamical Power Spectrum.
            Must be larger than the frequency resolution of the old Dynamical
            Power Spectrum!

        method: {``sum`` | ``mean`` | ``average``}, optional, default ``sum``
            This keyword argument sets whether the counts in the new bins
            should be summed or averaged.
        """
        dynspec_new = []
        for data in self.dyn_ps.T:
            freq_new, bin_counts, bin_err, _ = \
                utils.rebin_data(self.freq, data, dx_new=df_new,
                                 method=method)
            dynspec_new.append(bin_counts)

        self.freq = freq_new
        self.dyn_ps = np.array(dynspec_new).T
        self.df = df_new

    def trace_maximum(self, min_freq=None, max_freq=None, sigmaclip=False):
        """
        Return the indices of the maximum powers in each segment :class:`Powerspectrum`
        between specified frequencies.

        Parameters
        ----------
        min_freq: float, default ``None``
            The lower frequency bound.

        max_freq: float, default ``None``
            The upper frequency bound.

        Returns
        -------
        max_positions : np.array
            The array of indices of the maximum power in each segment having
            frequency between ``min_freq`` and ``max_freq``.
        """
        if min_freq is None:
            min_freq = np.min(self.freq)
        if max_freq is None:
            max_freq = np.max(self.freq)

        max_positions = []
        for ps in self.dyn_ps.T:
            indices = np.logical_and(self.freq <= max_freq,
                                     min_freq <= self.freq)
            max_power = np.max(ps[indices])
            max_positions.append(np.where(ps == max_power)[0][0])

        return np.array(max_positions)

    def rebin_time(self, dt_new, method='sum'):

        """
        Rebin the Dynamic Power Spectrum to a new time resolution.
        While the new resolution need not be an integer multiple of the
        previous time resolution, be aware that if it is not, the last bin
        will be cut off by the fraction left over by the integer division.

        Parameters
        ----------
        dt_new: float
            The new time resolution of the Dynamical Power Spectrum.
            Must be larger than the time resolution of the old Dynamical Power
            Spectrum!

        method: {"sum" | "mean" | "average"}, optional, default "sum"
            This keyword argument sets whether the counts in the new bins
            should be summed or averaged.


        Returns
        -------
        time_new: numpy.ndarray
            Time axis with new rebinned time resolution.

        dynspec_new: numpy.ndarray
            New rebinned Dynamical Power Spectrum.
        """

        if dt_new < self.dt:
            raise ValueError("New time resolution must be larger than "
                             "old time resolution!")

        dynspec_new = []
        for data in self.dyn_ps:
            time_new, bin_counts, bin_err, _ = \
                utils.rebin_data(self.time, data, dt_new,
                                 method=method)
            dynspec_new.append(bin_counts)

        self.time = time_new
        self.dyn_ps = np.array(dynspec_new)
        self.dt = dt_new
