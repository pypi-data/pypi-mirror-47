
import os, sys
import copy
import numpy as np
import healpy as hp

from astropy.time import Time

import gwemopt.utils
import gwemopt.rankedTilesGenerator
import gwemopt.scheduler
import ligo.segments as segments

def combine_coverage_structs(coverage_structs):

    coverage_struct_combined = {}
    coverage_struct_combined["data"] = np.empty((0,8))
    coverage_struct_combined["filters"] = np.empty((0,1))
    coverage_struct_combined["ipix"] = []
    coverage_struct_combined["patch"] = []
    coverage_struct_combined["FOV"] = np.empty((0,1))
    coverage_struct_combined["area"] = np.empty((0,1))
    coverage_struct_combined["telescope"] = np.empty((0,1))
    for coverage_struct in coverage_structs:
        coverage_struct_combined["data"] = np.append(coverage_struct_combined["data"],coverage_struct["data"],axis=0)
        coverage_struct_combined["filters"] = np.append(coverage_struct_combined["filters"],coverage_struct["filters"])
        coverage_struct_combined["ipix"] = coverage_struct_combined["ipix"] + coverage_struct["ipix"]
        coverage_struct_combined["patch"] = coverage_struct_combined["patch"] + coverage_struct["patch"]
        coverage_struct_combined["FOV"] = np.append(coverage_struct_combined["FOV"],coverage_struct["FOV"])
        coverage_struct_combined["area"] = np.append(coverage_struct_combined["area"],coverage_struct["area"])
        coverage_struct_combined["telescope"] = np.append(coverage_struct_combined["telescope"],coverage_struct["telescope"])
    return coverage_struct_combined

def read_coverage(params, telescope, filename):

    nside = params["nside"]
    config_struct = params["config"][telescope]

    lines = [line.rstrip('\n') for line in open(filename)]
    lines = lines[1:]
    lines = filter(None,lines)

    coverage_struct = {}
    coverage_struct["data"] = np.empty((0,8))
    coverage_struct["filters"] = []
    coverage_struct["ipix"] = []
    coverage_struct["patch"] = []
    coverage_struct["area"] = []

    for line in lines:
        lineSplit = line.split(",")
        ra = float(lineSplit[2])
        dec = float(lineSplit[3])
        mjd = float(lineSplit[4])
        filt = lineSplit[6]
        mag = float(lineSplit[7])

        coverage_struct["data"] = np.append(coverage_struct["data"],np.array([[ra,dec,mjd,mag,config_struct["exposuretime"],-1,-1,-1]]),axis=0)
        coverage_struct["filters"].append(filt)

        if telescope == "ATLAS":
            alpha=0.2
            color='#6c71c4'
        elif telescope == "PS1":
            alpha=0.1
            color='#859900'
        else:
            alpha=0.2
            color='#6c71c4'

        if config_struct["FOV_coverage_type"] == "square":
            ipix, radecs, patch, area = gwemopt.utils.getSquarePixels(ra, dec, config_struct["FOV_coverage"], nside, alpha=alpha, color=color)
        elif config_struct["FOV_coverage_type"] == "circle":
            ipix, radecs, patch, area = gwemopt.utils.getCirclePixels(ra, dec, config_struct["FOV_coverage"], nside, alpha=alpha, color=color)

        coverage_struct["patch"].append(patch)
        coverage_struct["ipix"].append(ipix)
        coverage_struct["area"].append(area)

    coverage_struct["filters"] = np.array(coverage_struct["filters"])
    coverage_struct["area"] = np.array(coverage_struct["area"])
    coverage_struct["FOV"] = config_struct["FOV_coverage"]*np.ones((len(coverage_struct["filters"]),))

    return coverage_struct

def read_coverage_files(params):

    coverage_structs = []
    for telescope, coverageFile in zip(params["telescopes"],params["coverageFiles"]):
        coverage_struct = read_coverage(params,telescope,coverageFile)
        coverage_structs.append(coverage_struct)

    return combine_coverage_structs(coverage_structs)

def waw(params, map_struct, tile_structs): 

    nside = params["nside"]

    t = np.arange(0,7,1/24.0)
    #t = np.arange(0,7,1.0)
    cr90 = map_struct["cumprob"] < 0.9
    detmaps = gwemopt.waw.detectability_maps(params, t, map_struct, verbose=True, limit_to_region=cr90, nside=nside)

    coverage_structs = []
    for telescope in params["telescopes"]: 
        tile_struct = tile_structs[telescope]
        config_struct = params["config"][telescope]
        T_int = config_struct["exposuretime"]
        ranked_tile_probs = gwemopt.tiles.compute_tiles_map(tile_struct, map_struct["prob"], func='np.sum(x)')
        strategy_struct = gwemopt.waw.construct_followup_strategy_tiles(map_struct["prob"],detmaps,t,tile_struct,T_int,params["Tobs"])
        if strategy_struct is None:
            raise ValueError("Change distance scale...")
        strategy_struct = strategy_struct*86400.0
        keys = tile_struct.keys()
        for key, prob, exposureTime in zip(keys, ranked_tile_probs, strategy_struct):
            tile_struct[key]["prob"] = prob
            tile_struct[key]["exposureTime"] = exposureTime
            tile_struct[key]["nexposures"] = int(np.floor(exposureTime/config_struct["exposuretime"]))
        coverage_struct = gwemopt.scheduler.scheduler(params, config_struct, tile_struct)
        coverage_structs.append(coverage_struct)

    if params["doPlots"]:
        gwemopt.plotting.waw(params,detmaps,t,strategy_struct)

    return combine_coverage_structs(coverage_structs)

def powerlaw(params, map_struct, tile_structs):

    map_struct_hold = copy.deepcopy(map_struct)

    coverage_structs = []
    n_scope = 0
    full_prob_map = map_struct["prob"]
    filters, exposuretimes = params["filters"], params["exposuretimes"]

    for telescope in params["telescopes"]:

        if params["doSplit"]:
            if "observability" in map_struct:
                map_struct["observability"][telescope]["prob"] = map_struct["groups"][n_scope]
            else:
                map_struct["prob"] = map_struct["groups"][n_scope]
            if n_scope < len(map_struct["groups"]) - 1:
                n_scope += 1
            else:
                n_scope = 0

        config_struct = params["config"][telescope]
        tile_struct = tile_structs[telescope]
        if "filt_change_time" in config_struct.keys(): filt_change_time = config_struct["filt_change_time"]
        else: filt_change_time = 0

        if params["doIterativeTiling"] and (params["tilesType"] == "galaxy"):
            tile_struct = gwemopt.utils.slice_galaxy_tiles(params, tile_struct, combine_coverage_structs(coverage_structs))

        if params["doAlternatingFilters"]:
            tile_struct_hold = copy.copy(tile_struct)
            coverage_structs_hold = []
            maxidx = 0
            for i in range(len(exposuretimes)):
                params["filters"] = [filters[i]]
                params["exposuretimes"] = [exposuretimes[i]]
                config_struct["exposurelist"] = segments.segmentlist(config_struct["exposurelist"][maxidx:])
                total_nexps  = len(config_struct["exposurelist"])

                # if the duration of a single block is less than 30 min, shift by additional time to add up to 30 min
                if i > 0:
                    start = Time(coverage_struct_hold["data"][0][2], format='mjd')
                    end =  Time(coverage_struct_hold["data"][-1][2], format='mjd')
                    delta = end - start
                    delta.format = 'sec'
                    duration = delta.value + exposuretimes[i] + filt_change_time
                    extra_time = (30 * 60) - duration
                    if extra_time > 0: extra_time = extra_time + filt_change_time
                    elif extra_time <= 0: extra_time = filt_change_time
                    config_struct["exposurelist"] = config_struct["exposurelist"].shift(extra_time / 86400.)

                if not params["tilesType"] == "galaxy":
                    tile_struct_hold = gwemopt.tiles.powerlaw_tiles_struct(params, config_struct, telescope, map_struct_hold, tile_struct_hold)      
                coverage_struct_hold = gwemopt.scheduler.scheduler(params, config_struct, tile_struct_hold)

                if len(coverage_struct_hold["exposureused"]) > 0:
                    maxidx = int(coverage_struct_hold["exposureused"][-1])
                    deltaL = total_nexps - maxidx
                elif len(coverage_struct_hold["exposureused"]) == 0: deltaL = 0

                coverage_structs_hold.append(coverage_struct_hold)
                if deltaL <= 1: break

            coverage_struct = combine_coverage_structs(coverage_structs_hold)
        else:
            if not params["tilesType"] == "galaxy":
                tile_struct = gwemopt.tiles.powerlaw_tiles_struct(params, config_struct, telescope, map_struct_hold, tile_struct)      
            coverage_struct = gwemopt.scheduler.scheduler(params, config_struct, tile_struct)

        coverage_structs.append(coverage_struct)

        if params["doIterativeTiling"]:
            map_struct_hold = gwemopt.utils.slice_map_tiles(params, map_struct_hold, coverage_struct)
                

    map_struct["prob"] = full_prob_map
    return combine_coverage_structs(coverage_structs)

def pem(params, map_struct, tile_structs):

    map_struct_hold = copy.deepcopy(map_struct)

    coverage_structs = []
    for telescope in params["telescopes"]:
        config_struct = params["config"][telescope]
        tile_struct = tile_structs[telescope]

        if params["doAlternatingFilters"]:
            filters, exposuretimes = params["filters"], params["exposuretimes"]
            tile_struct_hold = copy.copy(tile_struct)
            coverage_structs_hold = []
            for filt, exposuretime in zip(filters,exposuretimes):
                params["filters"] = [filt]
                params["exposuretimes"] = [exposuretime]
                tile_struct_hold = gwemopt.tiles.pem_tiles_struct(params, config_struct, telescope, map_struct_hold, tile_struct_hold)
                coverage_struct_hold = gwemopt.scheduler.scheduler(params, config_struct, tile_struct_hold)
                coverage_structs_hold.append(coverage_struct_hold)
            coverage_struct = combine_coverage_structs(coverage_structs_hold)
        else:
            tile_struct = gwemopt.tiles.pem_tiles_struct(params, config_struct, telescope, map_struct_hold, tile_struct)
            coverage_struct = gwemopt.scheduler.scheduler(params, config_struct, tile_struct)
        coverage_structs.append(coverage_struct)

        if params["doIterativeTiling"]:
            map_struct_hold = gwemopt.utils.slice_map_tiles(map_struct_hold, coverage_struct)

    return combine_coverage_structs(coverage_structs)

def timeallocation(params, map_struct, tile_structs):

    if params["timeallocationType"] == "powerlaw":
        print("Generating powerlaw schedule...")
        coverage_struct = gwemopt.coverage.powerlaw(params, map_struct, tile_structs)
    elif params["timeallocationType"] == "waw":
        if params["do3D"]:
            print("Generating WAW schedule...")
            coverage_struct = gwemopt.coverage.waw(params, map_struct, tile_structs)
        else:
            raise ValueError("Need to enable --do3D for waw")
    elif params["timeallocationType"] == "pem":
        print("Generating PEM schedule...")
        coverage_struct = gwemopt.coverage.pem(params, map_struct, tile_structs)

    return coverage_struct 
