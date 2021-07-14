import numpy as np
import skfuzzy as fuzz
import skfuzzy.membership as mf


def fuzzy_controller_v2(vac_percent, vac_rate):
    vac_percent *= 100
    vac_rate *= 100
    # define domains
    percent = np.arange(0, 100, 1)
    rate = np.arange(-100, 100, 1)
    delta = np.arange(-25, 25, 1)

    # partition sets
    percent_low = mf.trimf(percent, [0, 0, 50])
    percent_med = mf.trimf(percent, [25, 50, 65])
    percent_high = mf.trimf(percent, [50, 100, 100])

    rate_neg = mf.trimf(rate, [-100, -100, -30])
    rate_nz = mf.trimf(rate, [-50, 0, 50])
    rate_pos = mf.trimf(rate, [30, 100, 100])

    delta_neg_big = mf.trimf(delta, [-25, -25, -15])
    delta_neg = mf.trimf(delta, [-20, -10, 0])
    delta_nz = mf.trimf(delta, [-10, 0, 10])
    delta_pos = mf.trimf(delta, [0, 10, 20])
    delta_pos_big = mf.trimf(delta, [15, 25, 25])

    # apply membership functions
    percent_low_mb = fuzz.interp_membership(percent, percent_low, vac_percent)
    percent_med_mb = fuzz.interp_membership(percent, percent_med, vac_percent)
    percent_high_mb = fuzz.interp_membership(percent, percent_high, vac_percent)

    rate_neg_mb = fuzz.interp_membership(rate, rate_neg, vac_rate)
    rate_nz_mb = fuzz.interp_membership(rate, rate_nz, vac_rate)
    rate_pos_mb = fuzz.interp_membership(rate, rate_pos, vac_rate)

    # print(percent_low_mb,percent_med_mb,percent_high_mb)
    # print(rate_neg_mb,rate_nz_mb,rate_pos_mb)

    # define rules
    rule1 = np.fmin(percent_low_mb, delta_pos)
    rule2 = np.fmin(np.fmin(percent_low_mb, rate_nz_mb), delta_pos_big)
    rule3 = np.fmin(percent_med_mb, delta_pos)
    rule4 = np.fmin(np.fmin(percent_med_mb, rate_pos_mb), delta_neg)
    rule5 = np.fmin(np.fmin(percent_med_mb, rate_neg_mb), delta_pos)
    rule6 = np.fmin(np.fmin(percent_high_mb, rate_pos_mb), delta_neg_big)
    rule7 = np.fmin(percent_high_mb, delta_neg)

    # define
    delta_out_neg_big = rule6
    delta_out_neg = np.fmax(rule4, rule7)
    delta_out_nz = 0
    delta_out_pos = np.fmax(np.fmax(rule1, rule5), rule3)
    delta_out_pos_big = rule2

    # evaluate the controller output
    delta_out = np.fmax(np.fmax(np.fmax(delta_out_neg, delta_out_nz), np.fmax(delta_out_pos, delta_out_pos_big)),
                        delta_out_neg_big)
    defuzz = fuzz.defuzz(delta, delta_out, 'centroid')
    out = fuzz.interp_membership(delta, delta_out, defuzz)

    return defuzz / 100