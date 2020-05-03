#
# manita.py
#

from fastai.vision import *
from fastai.widgets import *
from google.colab import files

# 1. Setup path
path = Config.data_path() / "mushrooms"
print(f"Path: {path}")

# 2. Upload image urls
uploaded = files.upload()

# 3. Setup labels to search for
labels = [
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

# 4. Download images from urls
for label in labels:
    try:
        print(f"Downloading {label}")
        urls = label + ".txt"
        dest = path / label
        dest.mkdir(parents=True, exist_ok=True)
        files = download_images(urls, dest, max_pics=1000, timeout=10)
    except:
        print("Error while downloading")

# 5. Verify images
for label in labels:
    print(label)
    verify_images(path / label, delete=True)

# 6. Normalize images
np.random.seed(42)
data = ImageDataBunch.from_folder(
    path,
    train=".",
    valid_pct=0.2,
    ds_tfms=get_transforms(max_rotate=25, max_lighting=0.2, max_zoom=1.2),
    size=224,
    num_workers=4,
).normalize(imagenet_stats)

# 7. Print some information about dataset
print(f"Number of classes: {data.c}")
print(f"Name of classes: {data.classes}")
print(f"Length of train dataset: {len(data.train_ds)}")
print(f"Length of validation dataset: {len(data.valid_ds)}")

# 8. Explore dataset
data.show_batch(rows=3, figsize=(10, 10))

# 9. Build a classifier with ResNet34 model
learner = cnn_learner(data, models.resnet34, metrics=accuracy, callback_fns=ShowGraph)

# 10. Find learning rate
learner.lr_find()
learner.recorder.plot()

# 11. Fit model
learner.fit_one_cycle(16, max_lr=slice(1e-3, 1e-2))

# 12. Save model
learner.save("stage-1")

# 13. Export model
learner.export("model-0.1.0.pkl")
