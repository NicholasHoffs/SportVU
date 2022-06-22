def full_to_half_full(data):
    """
    Convert full court movement to a single half court
    Parameters
    ----------
    data: pandas.DataFrame
        dataframe containing SportVU movement data that covers the entire court
    Returns
    -------
    data: pandas.DataFrame
        dataframe containing SportVU movement data that
        is converted to a single half court (LOC_X < 47)
    """

    # first force all points above 47 to their half court counterparts
    # keep all original points for furhter limitations to single court
    data['LOC_X_original'] = data['LOC_X']
    data['LOC_Y_original'] = data['LOC_Y']
    data.loc[data.LOC_X > 47,'LOC_Y'] = data.loc[data.LOC_X > 47, 'LOC_Y'].apply(lambda y: 50 - y)
    data.loc[data.LOC_X > 47,'LOC_X'] = data.loc[data.LOC_X > 47, 'LOC_X'].apply(lambda x: 94 - x)

    return data

def half_full_to_half(data):
    """
    Convert single half court movement to shot log dimensional movement
    Parameters
    ----------
    data: pandas.DataFrame
        dataframe containing SportVU movement data that is converted to
        a single half court (LOC_X < 47)
    Returns
    -------
    data: pandas.DataFrame
        dataframe containing SportVU movement data that is converted
        to the single shooting court that follows shot log dimensions
        (-250-250, -47.5-422.5)
    """
    # convert to half court scale
    # note the LOC_X and the LOC_Y are switched in shot charts from movement data (charts are perpendicular)
    data['LOC_X_copy'] = data['LOC_X']
    data['LOC_Y_copy'] = data['LOC_Y']

    # Range conversion formula
    # http://math.stackexchange.com/questions/43698/range-scaling-problem

    data['LOC_X'] = data['LOC_Y_copy'].apply(lambda y: 250 * (1 - (y - 0)/(50 - 0)) + -250 * ((y - 0)/(50 - 0)))
    data['LOC_Y'] = data['LOC_X_copy'].apply(lambda x: -47.5 * (1 - (x - 0)/(47 - 0)) + 422.5 * ((x - 0)/(47 - 0)))
    data = data.drop(['LOC_X_copy', 'LOC_Y_copy'], axis=1, inplace=False)

    return data