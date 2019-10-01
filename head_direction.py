def moving_sum(array, window):
    ret = np.cumsum(array, dtype=float)
    ret[window:] = ret[window:] - ret[:-window]
    return ret[window:]


def get_rolling_sum(array_in, window):
    if window > (len(array_in) / 3) - 1:
        print('Window for head-direction histogram is too big, HD plot cannot be made.')
    inner_part_result = moving_sum(array_in, window)
    edges = np.append(array_in[-2 * window:], array_in[: 2 * window])
    edges_result = moving_sum(edges, window)
    end = edges_result[window:math.floor(len(edges_result)/2)]
    beginning = edges_result[math.floor(len(edges_result)/2):-window]
    array_out = np.hstack((beginning, inner_part_result, end))
    return array_out


def get_hd_histogram(angles):
    angles = angles[~np.isnan(angles)]
    theta = np.linspace(0, 2*np.pi, 361)  # x axis
    binned_hd, _, _ = plt.hist(angles, theta)
    smooth_hd = get_rolling_sum(binned_hd, window=23)
    return smooth_hd


# max firing rate at the angle where the firing rate is highest
def get_max_firing_rate(spatial_firing):
    max_firing_rates = []
    preferred_directions = []
    for index, cluster in spatial_firing.iterrows():
        hd_hist = cluster.hd_spike_histogram
        max_firing_rate = np.max(hd_hist.flatten())
        max_firing_rates.append(max_firing_rate)

        preferred_direction = np.where(hd_hist == max_firing_rate)
        preferred_directions.append(preferred_direction[0])

    spatial_firing['max_firing_rate_hd'] = np.array(max_firing_rates) / 1000  # Hz
    spatial_firing['preferred_HD'] = preferred_directions
    return spatial_firing


def get_hd_score_for_cluster(hd_hist):
    angles = np.linspace(-179, 180, 360)
    angles_rad = angles*np.pi/180
    dy = np.sin(angles_rad)
    dx = np.cos(angles_rad)

    totx = sum(dx * hd_hist)/sum(hd_hist)
    toty = sum(dy * hd_hist)/sum(hd_hist)
    r = np.sqrt(totx*totx + toty*toty)
    return r
