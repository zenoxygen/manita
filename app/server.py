import asyncio
import operator
import sys

from io import BytesIO

import aiohttp
import uvicorn

from fastai.vision import Path, load_learner, open_image
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

MODEL_URL = "https://manita.s3.eu-west-3.amazonaws.com/model-0.1.0.pkl"
MODEL_NAME = "model-0.1.0.pkl"

LABELS = [
    "agaricus_arvensis",
    "agaricus_augustus",
    "agaricus_bisporus",
    "agaricus_campestris",
    "albatrellus_confluens",
    "albatrellus_ovinus",
    "amanita_flavoconia",
    "amanita_fulva",
    "amanita_muscaria",
    "amanita_pantherina",
    "amanita_phalloides",
    "amanita_porphyria",
    "amanita_regalis",
    "amanita_rubescens",
    "amanita_virosa",
    "apioperdon_pyriforme",
    "armillaria_mellea",
    "artomyces_pyxidatus",
    "auriscalpium_vulgare",
    "bankera_fuligineoalba",
    "beefsteak_fungus",
    "bolbitius_titubans",
    "boletus_aereus",
    "boletus_badius",
    "boletus_edulis",
    "boletus_pinophilus",
    "boletus_satanas",
    "boletus_subtomentosus",
    "bondarzewia_berkeleyi",
    "bovista_plumbea",
    "calocera_viscosa",
    "calocybe_gambosa",
    "calocybe_persicolor",
    "candelaria_concolor",
    "cantharellula_umbonata",
    "cantharellus_cascadensis",
    "cantharellus_cibarius",
    "cantharellus_cinnabarinus",
    "cantharellus_formosus",
    "cantharellus_lateritius",
    "cantharellus_minor",
    "cantharellus_roseocanus",
    "cantharellus_subalbidus",
    "cerioporus_squamosus",
    "chalciporus_piperatus",
    "chlorophyllum_molybdites",
    "clitocybe_clavipes",
    "clitocybe_gibba",
    "clitocybe_nebularis",
    "clitopilus_prunulus",
    "collybia_dryophila",
    "coltricia_perennis",
    "coprinellus_disseminatus",
    "coprinellus_micaceus",
    "coprinopsis_atramentaria",
    "coprinopsis_lagopus",
    "coprinus_comatus",
    "coprinus_plicatilis",
    "cortinarius_alboviolaceus",
    "cortinarius_armillatus",
    "cortinarius_caperatus",
    "cortinarius_collinitus",
    "cortinarius_croceus",
    "cortinarius_laniger",
    "cortinarius_malicorius",
    "cortinarius_mucosus",
    "cortinarius_orellanus",
    "cortinarius_rubellus",
    "cortinarius_semisanguineus",
    "cortinarius_traganus",
    "craterellus_cornucopioides",
    "craterellus_tubaeformis",
    "cystoderma_amianthinum",
    "dacrymyces_chrysospermus",
    "entoloma_sericeum",
    "evernia_prunastri",
    "flavoparmelia_caperata",
    "fomes_fomentarius",
    "fomitopsis_betulina",
    "fomitopsis_pinicola",
    "galerina_marginata",
    "ganoderma_applanatum",
    "gomphidius_glutinosus",
    "gomphus_clavatus",
    "gyromitra_esculenta",
    "gyromitra_infula",
    "hebeloma_crustuliniforme",
    "hebeloma_mesophaeum",
    "hericium_erinaceus",
    "hydnum_repandum",
    "hydnum_rufescens",
    "hygrophoropsis_aurantiaca",
    "hygrophorus_camarophyllus",
    "hygrophorus_hypothejus",
    "hypholoma_capnoides",
    "hypholoma_fasciculare",
    "hypholoma_marginatum",
    "inocybe_lacera",
    "kuehneromyces_mutabilis",
    "laccaria_laccata",
    "lactarius_camphoratus",
    "lactarius_deliciosus",
    "lactarius_deterrimus",
    "lactarius_helvus",
    "lactarius_lignyotus",
    "lactarius_mammosus",
    "lactarius_rufus",
    "lactarius_tabidus",
    "lactarius_torminosus",
    "lactarius_trivialis",
    "lactarius_turpis",
    "lactarius_volemus",
    "laetiporus_sulphureus",
    "leccinum_aurantiacum",
    "leccinum_scabrum",
    "leccinum_versipelle",
    "lepista_nuda",
    "lobaria_pulmonaria",
    "lycoperdon_excipuliforme",
    "lycoperdon_nigrescens",
    "lycoperdon_perlatum",
    "lycoperdon_pyriforme",
    "macrolepiota_procera",
    "macrolepiota_rachodes",
    "marasmius_oreades",
    "megacollybia_platyphylla",
    "melanoleuca_cognata",
    "mitrophora_semilibera",
    "morchella_angusticeps",
    "morchella_conica",
    "morchella_costata",
    "morchella_crassipes",
    "morchella_deliciosa",
    "morchella_dunensis",
    "morchella_elata",
    "morchella_esculenta",
    "morchella_hortensis",
    "morchella_rotunda",
    "mycena_galericulata",
    "mycena_pura",
    "otidea_onotica",
    "parasola_plicatilis",
    "parmelia_sulcata",
    "paxillus_atrotomentosus",
    "paxillus_involutus",
    "phaeolus_schweinitzii",
    "phallus_rubicundus",
    "pholiota_alnicola",
    "pholiota_aurivella",
    "pholiota_squarrosa",
    "pleurotus_eryngii",
    "pleurotus_ostreatus",
    "pluteus_cervinus",
    "polyporus_ciliatus",
    "polyporus_squamosus",
    "psathyrella_candolleana",
    "psilocybe_semilanceata",
    "rhizina_undulata",
    "rickenella_swartzii",
    "russula_acrifolia",
    "russula_aeruginea",
    "russula_aurea",
    "russula_claroflava",
    "russula_cyanoxantha",
    "russula_decolorans",
    "russula_emetica",
    "russula_obscura",
    "russula_paludosa",
    "russula_vesca",
    "russula_virescens",
    "russula_xerampelina",
    "sarcodon_squamosus",
    "schizophyllum_commune",
    "scleroderma_citrinum",
    "stereum_complicatum",
    "stereum_hirsutum",
    "stereum_ostrea",
    "strobilurus_esculentus",
    "strobilurus_stephanocystis",
    "stropharia_hornemannii",
    "suillus_bovinus",
    "suillus_grevillei",
    "suillus_luteus",
    "suillus_variegatus",
    "trametes_versicolor",
    "tremella_mesenterica",
    "trichaptum_biforme",
    "tricholoma_flavovirens",
    "tricholoma_focale",
    "tricholoma_saponaceum",
    "tricholoma_sejunctum",
    "tricholomopsis_decora",
    "tricholomopsis_rutilans",
    "tuber_aestivum",
    "tuber_borchii",
    "tuber_magnatum",
    "tuber_melanosporum",
    "turbinellus_floccosus",
    "tylopilus_felleus",
    "xanthoria_parietina",
]

path = Path(__file__).parent

app = Starlette()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["X-Requested-With", "Content-Type"],
)
app.mount("/static", StaticFiles(directory="app/static"))


async def download_file(url, dest):
    """
    Download file.
    """
    if dest.exists():
        return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, "wb") as f:
                f.write(data)


async def setup_learner():
    """
    Setup learner.
    """
    await download_file(MODEL_URL, path / MODEL_NAME)
    try:
        learner = load_learner(path, MODEL_NAME)
        return learner
    except RuntimeError as e:
        if len(e.args) > 0 and "CPU-only machine" in e.args[0]:
            print(e)
            message = "This model was trained with an old version of fastai \
                and will not work in a CPU environment. Please update the \
                fastai library in your training environment and export your \
                model again."
            raise RuntimeError(message)
        else:
            raise


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learner = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


def percent(v):
    """
    Transform probability into percentage.
    """
    return v * 100


@app.route("/")
async def homepage(request):
    """
    Homepage.
    """
    html_file = path / "view" / "index.html"
    return HTMLResponse(html_file.open().read())


@app.route("/analyze", methods=["POST"])
async def analyze(request):
    """
    Analyze an image.
    """
    # Get image
    img_data = await request.form()
    img_bytes = await (img_data["file"].read())
    img = open_image(BytesIO(img_bytes))

    # Load model
    learner = load_learner(path, MODEL_NAME)

    # Make predictions
    pred_class, pred_idx, outputs = learner.predict(img)

    # Get predicted class
    result = str(pred_class).capitalize()

    # Combine labels and outputs probabilities
    predictions = dict(zip(LABELS, outputs.tolist()))

    # Transform predictions into percentages
    predictions = dict((k, percent(v)) for k, v in predictions.items())

    # Sort predictions in descending order
    predictions = dict(
        sorted(predictions.items(), key=operator.itemgetter(1), reverse=True)
    )

    # Keep only 3 best predictions
    predictions = dict(list(predictions.items())[0:3])

    # Format predictions
    labels = list(map(lambda x: x.replace("_", " ").capitalize(),
                      predictions.keys()))
    data = list(predictions.values())

    return JSONResponse({"result": result, "labels": labels, "data": data})


if __name__ == "__main__":
    if "serve" in sys.argv:
        uvicorn.run(app=app, host="0.0.0.0", port=5000, log_level="info")
