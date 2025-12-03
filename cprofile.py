from robotpy.main import main

if __name__ == "__main__":
    import cProfile, pstats, sys
    profiler = cProfile.Profile()
    profiler.enable()
    try:
        main()
    except:
        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('cumtime')
        stats.print_stats()
