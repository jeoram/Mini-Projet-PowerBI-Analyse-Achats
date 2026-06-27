# Mini-Projet Power BI - Analyse Achats

## 🎯 Contexte
Analyse et visualisation des performances achats : panel fournisseurs, KPIs opérationnels, financiers et RSE.
Ce dashboard permet d'aider la prise de décision pour la Direction Achats.

## 🛠 Technologies utilisées
- Power BI Desktop (modélisation, DAX, visualisation)
- Power Query (nettoyage et transformation)
- Dataset : Procurement KPI Analysis (Kaggle)
- Python pour l'EDA et la préparation des KPI
- Git & GitHub (versionning)

## 📊 Fonctionnalités du Dashboard
- Vue globale des achats (Spend, OTD, Savings)
- Performance par fournisseur (Top/Bottom, segmentation ABC)
- Analyse RSE et bas carbone
- Évolution temporelle
- Filtres interactifs et drill-down

## 📁 Contenu du Repository
- data/ → Données sources et exemples de fichiers CSV
- pbix/ → Fichier .pbix complet
- screenshots/ → Captures d'écran détaillées du processus
- documentation/ → Rapport complet du projet
- scripts/ → Scripts Python d'EDA et de génération de KPI

## 🚀 Comment utiliser
1. Télécharger le fichier .pbix
2. Ouvrir avec Power BI Desktop
3. Explorer les différentes pages du rapport
4. Si vous souhaitez reproduire l'EDA, exécuter le script Python depuis la racine du projet :
   python scripts/eda_kpi.py

## 📸 Aperçu du Dashboard
![Vue Globale](screenshots/01_Page_Accueil.png)

## 🔑 KPIs développés
- Spend Total & Savings %
- On-Time Delivery (OTD %)
- Taux de Qualité
- Score RSE pondéré
- Concentration des achats (Top 10 %)
- Nombre de fournisseurs actifs

## 🧪 EDA Python fournie
Le script Python dans [scripts/eda_kpi.py](scripts/eda_kpi.py) prépare automatiquement :
- un fichier de KPI globaux,
- un fichier de KPI par fournisseur,
- un fichier de KPI par période si une colonne de date est présente.

Pour générer des visualisations directement depuis Python, exécutez :
python scripts/visualize_kpi.py

Les graphiques seront exportés dans [outputs/plots](outputs/plots).

## 📈 KPIs recommandés à intégrer dans Power BI
Pour la partie Power BI, les KPI suivants sont particulièrement utiles :
- Spend Total
- Savings Amount
- Savings %
- OTD %
- Quality %
- RSE Score
- Top 10% Spend Concentration
- Supplier Count

## 🔗 Source de la base de données
Procurement KPI Analysis Dataset : https://www.kaggle.com/datasets/shahriarkabir/procurement-kpi-analysis-dataset?resource=download
