#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 14:56:02 2021

@author:
Dr. Maximilian N. Günther
European Space Agency (ESA)
European Space Research and Technology Centre (ESTEC)
Keplerlaan 1, 2201 AZ Noordwijk, The Netherlands
Email: maximilian.guenther@esa.int
GitHub: mnguenther
Twitter: m_n_guenther
Web: www.mnguenther.com
"""

import allesfitter

# Current file directory
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

# For non-TTV fits:
# allesfitter.show_initial_guess('allesfit_ephemerides')
# allesfitter.ns_fit('allesfit_ephemerides')
# allesfitter.ns_output('allesfit_ephemerides')


# For TTV fits:
# allesfitter.prepare_ttv_fit('allesfit_with_ttvs')
# allesfitter.show_initial_guess('allesfit_with_ttvs')
# allesfitter.ns_fit('allesfit_with_ttvs')
# allesfitter.ns_output('allesfit_with_ttvs')

# with TTVS = b_ttv_transit_1,0,1,uniform -0.04167 0.04167,TTV$_\mathrm{b;1}$,d,
# allesfitter.show_initial_guess('allesfit_with_ttvs_1hour')
# allesfitter.ns_fit('allesfit_with_ttvs_1hour')
# allesfitter.ns_output('allesfit_with_ttvs_1hour')


# For multi instrument fits:
# allesfitter.prepare_ttv_fit('allesfit_with_ttvs')
# allesfitter.show_initial_guess('allesfit_ephemerides_only_first_4_tess_bjd')
# allesfitter.ns_fit('allesfit_ephemerides_only_first_4_tess_bjd')
# allesfitter.ns_output('allesfit_ephemerides_only_first_4_tess_bjd')


# allesfitter.show_initial_guess('allesfit_ephemerides_chat')
# allesfitter.ns_fit('allesfit_ephemerides_chat')
# allesfitter.ns_output('allesfit_ephemerides_chat')


# allesfitter.show_initial_guess('allesfit_ephemerides_multi_instrument-tests')
# allesfitter.ns_fit('allesfit_ephemerides_multi_instrument-tests')
# allesfitter.ns_output('allesfit_ephemerides_multi_instrument-tests')


# allesfitter.show_initial_guess('allesfit_ephemerides_multi_instrument')
# allesfitter.ns_fit('allesfit_ephemerides_multi_instrument')
# allesfitter.ns_output('allesfit_ephemerides_multi_instrument')

dirname = "allesfit_ephemerides_multi_instrument_tess_fixed_params"
dirname = "allesfit_ephemerides_multi_instrument_astepchatomes_fixed_params"
dirname = "allesfit_with_ttvs"
dirname = "allesfit_ttvs_multi_instrument_tess_fixed_params"
dirname = "allesfit_ttvs_multi_instrument_astepchatomes_fixed_params"


allesfitter.show_initial_guess(dirname)
allesfitter.ns_fit(dirname)
allesfitter.ns_output(dirname)
