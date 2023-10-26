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
allesfitter.show_initial_guess('allesfit_with_ttvs')
allesfitter.ns_fit('allesfit_with_ttvs')
allesfitter.ns_output('allesfit_with_ttvs')
