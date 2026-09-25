# Meteor-Hackable

Fichiers, scripts et organigrammes accompagnant l'article :  
**« Meteor-M et LRPT : recevoir et décoder les nouvelles images météo »** (Thomas Lavarenne, *Hackable Magazine*).

Ce dépôt permet de reproduire l'intégralité de la chaîne de traitement du protocole **LRPT** des satellites météorologiques russes **Meteor-M (No. 2-3 et No. 2-4)** : de la réception du signal RF à la reconstruction et l'affichage des images satellite JPEG.

---

## 📁 Structure du dépôt

```text
Meteor-Hackable/
├── gnuradio/
│   └── meteor.grc          # Organigramme GNU Radio (démodulation OQPSK, boucle de Costas, synchro symbole)
├── viterbi/
│   ├── jmf_viterb.c        # Programme en C pour le décodage de Viterbi (K=7, taux 1/2) via libfec
│   ├── jmf_viterb          # Binaire compilé prêt à l'emploi (Linux x86_64)
│   └── Makefile            # Instructions de compilation du décodeur Viterbi
├── python/
│   ├── decode_meteor.py    # Décodeur complet pas à pas (rotation soft bits, Viterbi, décodage différentiel, synchro, désembrouillage PN)
│   └── extract_viterbi.py  # Fonctions de décompression JPEG (Huffman, TCDI inverse, matrice zig-zag, affichage imagettes)
├── captures/
│   ├── binarymeteor.s      # Échantillon de soft-bits démodulés pour test immédiat
│   ├── meteorn2_3x.s       # Capture d'un passage Meteor-M No. 2-3 / 2-4
│   ├── entreeViterbi.bin   # Fichier d'entrée pour le module Viterbi
│   └── sortieViterbi.bin   # Fichier de sortie décodé par Viterbi
```

---

## ⚙️ Prérequis

### 1. Python et dépendances
Installez les bibliothèques nécessaires avec `pip` :

```bash
pip install -r requirements.txt
```

*(Numpy, Scipy, Pillow, Matplotlib)*

### 2. Décodeur Viterbi en C
Le dossier `viterbi/` contient l'exécutable précompilé `jmf_viterb`. Si vous devez le recompiler sur votre machine :

```bash
cd viterbi
make
cd ..
```

*Note : la compilation s'appuie sur la bibliothèque `libfec` de Phil Karn (ou `libcorrect`).*

---

## 🚀 Utilisation pas à pas

### Étape 1 : Démodulation radio sous GNU Radio
Le fichier `gnuradio/meteor.grc` implémente la démodulation du signal radio reçu sur 137,1 MHz ou 137,9 MHz :
* Réception SDR (RTL-SDR, HackRF, USRP...)
* Filtrage passe-bas et RRC (*Root Raised Cosine*)
* Synchronisation porteuse (Boucle de Costas OQPSK)
* Récupération d'horloge symbole (*Symbol Sync*)
* Enregistrement des **soft bits** entrelacés (format `int8`) dans un fichier binaire `.s`.

### Étape 2 : Décodage complet des trames LRPT
Le script `python/decode_meteor.py` enchaîne automatiquement les étapes décrites dans l'article :
1. Extraction et rotation des voies I/Q (`rotate_softbits`)
2. Décodage convolutionnel par l'algorithme de Viterbi (`run_viterbi`)
3. Décodage différentiel pour lever l'ambiguïté de phase résiduelle (`differential_decode`)
4. Recherche du mot de synchronisation unique `0x1ACFFC1D` (espacé de 8192 bits = 1024 octets)
5. Désembrouillage par XOR avec la séquence pseudo-aléatoire (PN) de 255 octets
6. Identification des trames et des canaux (APID 64 = Canal 1 visible, APID 65 = Canal 2 proche IR, APID 66 = Canal 3 IR court).

Pour lancer le décodage sur la capture de test fournie :

```bash
python3 python/decode_meteor.py captures/binarymeteor.s
```

Ou sur un enregistrement plus long :

```bash
python3 python/decode_meteor.py captures/meteorn2_3x.s --samples 800000
```

Exemple de sortie :
```text
Chargement de captures/meteorn2_3x.s...
Soft-bits analysés : 800000
Décodage Viterbi (K=7, R=1/2)...
Bits décodés : 409600 (1: 199482, 0: 210118)
Mots de synchronisation 0x1ACFFC1D détectés : 40
Espacements observés (attendu = 8192 bits = 1024 octets) : [8192  8192  8192  8192  8192]
Trame #01 | APID=64 (Canal 1 (Visible)) | pointeur=645
Trame #02 | APID=64 (Canal 1 (Visible)) | pointeur=321
...
Total de trames extraites avec succès : 40
```

### Étape 3 : Décompression JPEG et affichage des imagettes
Le module `python/extract_viterbi.py` détaille la reconstruction des blocs d'images :
* Décompression de Huffman
* Rangement de la matrice 8×8 en zig-zag
* Dé-quantification
* Transformée en cosinus discrète inverse (TCDI)
* Assemblage des imagettes selon leurs index de trame pour reconstituer la vue géographique globale.

---

## 📚 Références & Liens utiles

* **Article de référence :** Thomas Lavarenne, *« Meteor-M et LRPT : recevoir et décoder les nouvelles images météo »*, *Hackable Magazine*.
* **Articles fondateurs :** Jean-Michel Friedt, *« Décodage d’images numériques issues de satellites météorologiques en orbite basse : le protocole LRPT de Meteor-M2 »*, GNU/Linux Magazine France n°226, 227 et 228 (2019).
* **SatDump :** [https://github.com/SatDump/SatDump](https://github.com/SatDump/SatDump)
* **Bibliothèque libfec :** Phil Karn, [https://github.com/ka9q/libfec](https://github.com/ka9q/libfec)
