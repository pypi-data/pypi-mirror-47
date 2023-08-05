import logging
import chaospy as cp
from easyvvuq import OutputType
from .base import BaseAnalysisElement

# author: Jalal Lakhlili
__license__ = "LGPL"

logger = logging.getLogger(__name__)

# TODO:
# 1. Work out how to get multiple Sobol indices
# 1. a. Note that may require different orders for different qoi?
# 2. Add pd.read_hdf (https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-hdf5).
# 3. Test cp.fit_regression to approximate solver.


class PCEAnalysis(BaseAnalysisElement):

    def element_name(self):
        return "PCE_Analysis"

    def element_version(self):
        return "0.3"

    def __init__(self, params_cols=None, sampler=None, qoi_cols=None,
                 sobol_order=1):

        if sampler is None:
            msg = 'PCE analysis requires a paired sampler to be passed'
            raise RuntimeError(msg)

        if qoi_cols is None:
            raise RuntimeError("Analysis element requires a list of "
                               "quantities of interest (qoi)")

        if sobol_order > len(sampler.vary.vary_dict):
            logger.warning("sobol_order too high - set to number of "
                           "variables from sampler")
            sobol_order = len(sampler.vary.vary_dict)

        self.sobol_order = sobol_order
        self.params_cols = params_cols
        self.qoi_cols = qoi_cols
        self.output_type = OutputType.SUMMARY
        self.sampler = sampler

    def analyse(self, data_frame=None):

        if data_frame is None:
            raise RuntimeError("Analysis element needs a data frame to "
                               "analyse")

        qoi_cols = self.qoi_cols

        results = {'statistical_moments': {},
                   'percentiles': {},
                   'sobol_indices': {k: {} for k in qoi_cols},
                   'correlation_matrices': {},
                   'output_distributions': {},
                   }

        # Get the Polynomial
        P = self.sampler.P

        # Compute nodes and weights
        nodes, weights = cp.generate_quadrature(order=self.sampler.quad_order,
                                                domain=self.sampler.distribution,
                                                rule=self.sampler.quad_rule,
                                                sparse=self.sampler.quad_sparse)

        # Extract output values for each quantity of interest from Dataframe
        samples = {k: [] for k in qoi_cols}
        for run_id in data_frame.run_id.unique():
            for k in qoi_cols:
                values = data_frame.loc[data_frame['run_id'] == run_id][k]
                samples[k].append(values)

        output_distributions = {}

        # Compute descriptive statistics for each quantity of interest
        for k in qoi_cols:
            # Approximation solver
            fit = cp.fit_quadrature(P, nodes, weights, samples[k])

            # Statistical moments
            mean = cp.E(fit, self.sampler.distribution)
            var = cp.Var(fit, self.sampler.distribution)
            std = cp.Std(fit, self.sampler.distribution)
            results['statistical_moments'][k] = {'mean': mean,
                                                 'var': var,
                                                 'std': std}

            # Percentiles (Pxx)
            P10 = cp.Perc(fit, 10, self.sampler.distribution)
            P90 = cp.Perc(fit, 90, self.sampler.distribution)
            results['percentiles'][k] = {'p10': P10, 'p90': P90}

            # First Sobol indices
            # TODO: Implement higher order indices
            logger.warning('Only first order Sobol indices implemented')
            sobol_first_narr = cp.Sens_m(fit, self.sampler.distribution)
            sobol_first_dict = {}
            i_par = 0
            for param_name in self.sampler.vary.get_keys():
                sobol_first_dict[param_name] = sobol_first_narr[i_par]
                i_par += 1
            # 1 here = order
            results['sobol_indices'][k][1] = sobol_first_dict

            # Correlation matrix
            results['correlation_matrices'][k] = cp.Corr(
                fit, self.sampler.distribution)

            # Output distributions
            results['output_distributions'][k] = cp.QoI_Dist(
                fit, self.sampler.distribution)

        return results
