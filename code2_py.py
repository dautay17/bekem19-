# -*- coding: utf-8 -*-
"""code2.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QIX0wMoVbUOEeIW6oQ54UCk4rBbW3wnA
"""

import streamlit as st
import pandas as pd
import numpy as np
chart_data= pd.DataFrame(np.random.rand(20,3),columns=['a','b','c'])
st.bar_chart(chart_data)