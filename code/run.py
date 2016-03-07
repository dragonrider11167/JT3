from framebase import frame
import logger, json
globals().update(logger.build_module_logger("run"))

debug("Starting...")

with open("engine.cfg", 'r') as fd:
    engine_config=json.load(fd)

debug("engine_config = "+str(engine_config))

info("Preloading core "+engine_config["main_provider"])
frame.loader._selected.append(engine_config["main_provider_path"])
frame.loader.load_selected()

info("Running preinit on core "+engine_config["main_provider"])
frame.modules[engine_config["main_provider"]].preinit()

for item in engine_config["load_order"]:
    debug("Adding directory "+item)
    frame.loader.add_directory(item)

debug("Loading...")
frame.loader.load_selected()

info("Starting core "+engine_config["main_provider"])
frame.modules[engine_config["main_provider"]].run_main()
