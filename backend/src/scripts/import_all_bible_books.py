"""
Complete list of all 66 Bible books for import.
This file contains the mapping of all books from the GitHub repository.
"""

# Old Testament (39 books)
OLD_TESTAMENT_BOOKS = [
    # Pentateuch (Torah)
    {"file": "genesisy.json", "nom": "Genesisy", "abbrev": "Gen", "ordre": 1},
    {"file": "eksodosy.json", "nom": "Eksodosy", "abbrev": "Eks", "ordre": 2},
    {"file": "levitika.json", "nom": "Levitika", "abbrev": "Lev", "ordre": 3},
    {"file": "nomery.json", "nom": "Nomery", "abbrev": "Nom", "ordre": 4},
    {"file": "detoronomy.json", "nom": "Detoronomy", "abbrev": "Deo", "ordre": 5},

    # Historical Books
    {"file": "josoa.json", "nom": "Josoa", "abbrev": "Jos", "ordre": 6},
    {"file": "mpitsara.json", "nom": "Mpitsara", "abbrev": "Mts", "ordre": 7},
    {"file": "rota.json", "nom": "Rota", "abbrev": "Rot", "ordre": 8},
    {"file": "1_samoela.json", "nom": "1 Samoela", "abbrev": "1Sam", "ordre": 9},
    {"file": "2_samoela.json", "nom": "2 Samoela", "abbrev": "2Sam", "ordre": 10},
    {"file": "1_mpanjaka.json", "nom": "1 Mpanjaka", "abbrev": "1Mpj", "ordre": 11},
    {"file": "2_mpanjaka.json", "nom": "2 Mpanjaka", "abbrev": "2Mpj", "ordre": 12},
    {"file": "1_tantara.json", "nom": "1 Tantara", "abbrev": "1Tan", "ordre": 13},
    {"file": "2_tantara.json", "nom": "2 Tantara", "abbrev": "2Tan", "ordre": 14},
    {"file": "ezra.json", "nom": "Ezra", "abbrev": "Ezr", "ordre": 15},
    {"file": "nehemia.json", "nom": "Nehemia", "abbrev": "Neh", "ordre": 16},
    {"file": "estera.json", "nom": "Estera", "abbrev": "Est", "ordre": 17},

    # Wisdom Books
    {"file": "joba.json", "nom": "Joba", "abbrev": "Job", "ordre": 18},
    {"file": "salamo.json", "nom": "Salamo", "abbrev": "Sal", "ordre": 19},
    {"file": "ohabolana.json", "nom": "Ohabolana", "abbrev": "Oha", "ordre": 20},
    {"file": "mpitoriteny.json", "nom": "Mpitoriteny", "abbrev": "Mpi", "ordre": 21},
    {"file": "tonon-kiran_i_solomona.json", "nom": "Tonon-kiran'i Solomona", "abbrev": "Ton", "ordre": 22},

    # Major Prophets
    {"file": "isaia.json", "nom": "Isaia", "abbrev": "Isa", "ordre": 23},
    {"file": "jeremia.json", "nom": "Jeremia", "abbrev": "Jer", "ordre": 24},
    {"file": "fitomaniana.json", "nom": "Fitomaniana", "abbrev": "Fit", "ordre": 25},
    {"file": "ezekiela.json", "nom": "Ezekiela", "abbrev": "Eze", "ordre": 26},
    {"file": "daniela.json", "nom": "Daniela", "abbrev": "Dan", "ordre": 27},

    # Minor Prophets
    {"file": "hosea.json", "nom": "Hosea", "abbrev": "Hos", "ordre": 28},
    {"file": "joela.json", "nom": "Joela", "abbrev": "Joe", "ordre": 29},
    {"file": "amosa.json", "nom": "Amosa", "abbrev": "Amo", "ordre": 30},
    {"file": "obadia.json", "nom": "Obadia", "abbrev": "Oba", "ordre": 31},
    {"file": "jona.json", "nom": "Jona", "abbrev": "Jon", "ordre": 32},
    {"file": "mika.json", "nom": "Mika", "abbrev": "Mik", "ordre": 33},
    {"file": "nahoma.json", "nom": "Nahoma", "abbrev": "Nah", "ordre": 34},
    {"file": "habakoka.json", "nom": "Habakoka", "abbrev": "Hab", "ordre": 35},
    {"file": "zefania.json", "nom": "Zefania", "abbrev": "Zef", "ordre": 36},
    {"file": "hagay.json", "nom": "Hagay", "abbrev": "Hag", "ordre": 37},
    {"file": "zakaria.json", "nom": "Zakaria", "abbrev": "Zak", "ordre": 38},
    {"file": "malakia.json", "nom": "Malakia", "abbrev": "Mal", "ordre": 39},
]

# New Testament (27 books)
NEW_TESTAMENT_BOOKS = [
    # Gospels
    {"file": "matio.json", "nom": "Matio", "abbrev": "Mat", "ordre": 40},
    {"file": "marka.json", "nom": "Marka", "abbrev": "Mar", "ordre": 41},
    {"file": "lioka.json", "nom": "Lioka", "abbrev": "Lio", "ordre": 42},
    {"file": "jaona.json", "nom": "Jaona", "abbrev": "Jao", "ordre": 43},

    # Acts
    {"file": "asan_ny_apostoly.json", "nom": "Asan'ny Apostoly", "abbrev": "Asa", "ordre": 44},

    # Paul's Letters
    {"file": "romana.json", "nom": "Romana", "abbrev": "Rom", "ordre": 45},
    {"file": "1_korintianina.json", "nom": "1 Korintianina", "abbrev": "1Kor", "ordre": 46},
    {"file": "2_korintianina.json", "nom": "2 Korintianina", "abbrev": "2Kor", "ordre": 47},
    {"file": "galatianina.json", "nom": "Galatianina", "abbrev": "Gal", "ordre": 48},
    {"file": "efesianina.json", "nom": "Efesianina", "abbrev": "Efe", "ordre": 49},
    {"file": "filipianina.json", "nom": "Filipianina", "abbrev": "Fil", "ordre": 50},
    {"file": "kolosianina.json", "nom": "Kolosianina", "abbrev": "Kol", "ordre": 51},
    {"file": "1_tesalonianina.json", "nom": "1 Tesalonianina", "abbrev": "1Tes", "ordre": 52},
    {"file": "2_tesalonianina.json", "nom": "2 Tesalonianina", "abbrev": "2Tes", "ordre": 53},
    {"file": "1_timoty.json", "nom": "1 Timoty", "abbrev": "1Tim", "ordre": 54},
    {"file": "2_timoty.json", "nom": "2 Timoty", "abbrev": "2Tim", "ordre": 55},
    {"file": "titosy.json", "nom": "Titosy", "abbrev": "Tit", "ordre": 56},
    {"file": "filemona.json", "nom": "Filemona", "abbrev": "Fle", "ordre": 57},

    # General Letters
    {"file": "hebreo.json", "nom": "Hebreo", "abbrev": "Heb", "ordre": 58},
    {"file": "jakoba.json", "nom": "Jakoba", "abbrev": "Jak", "ordre": 59},
    {"file": "1_petera.json", "nom": "1 Petera", "abbrev": "1Pet", "ordre": 60},
    {"file": "2_petera.json", "nom": "2 Petera", "abbrev": "2Pet", "ordre": 61},
    {"file": "1_jaona.json", "nom": "1 Jaona", "abbrev": "1Jao", "ordre": 62},
    {"file": "2_jaona.json", "nom": "2 Jaona", "abbrev": "2Jao", "ordre": 63},
    {"file": "3_jaona.json", "nom": "3 Jaona", "abbrev": "3Jao", "ordre": 64},
    {"file": "joda.json", "nom": "Joda", "abbrev": "Jod", "ordre": 65},

    # Prophecy
    {"file": "apokalypsy.json", "nom": "Apokalypsy", "abbrev": "Apo", "ordre": 66},
]

def get_all_books():
    """Return all 66 Bible books."""
    return OLD_TESTAMENT_BOOKS, NEW_TESTAMENT_BOOKS
