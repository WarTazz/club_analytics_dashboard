{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "6b9041f0-e72c-4db4-a371-4423dad677e7",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import ipywidgets as widgets\n",
    "from IPython.display import display"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "d4a1e479-5965-4744-9d9b-65c9ed3367f7",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Charger la feuille nommée 'Sheet1' du fichier Excel\n",
    "df = pd.read_excel('/Users/thomas/Documents/Études/Master_EOPS/Stage APER & SRR/2023-2024/Monitoring/RPE_EDF/Sauvegardes/V4 mars 2024.xlsx', sheet_name='BD EDF')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "b16bd532-1d82-4f1e-9511-eb4b4266825b",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "import locale\n",
    "\n",
    "# Définir la locale française pour les dates\n",
    "locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')\n",
    "\n",
    "# Convertir la colonne de dates en datetime si nécessaire\n",
    "df['Date'] = pd.to_datetime(df['Date'])\n",
    "\n",
    "# Supprimer la colonne Horodateur\n",
    "# df.drop(\"Horodateur\", axis=1, inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "e2f052c5-c5c0-4849-a3a8-c778f05cdee4",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "# Extraire l'année et le numéro de semaine de la colonne de dates\n",
    "df['Année'] = df['Date'].dt.year\n",
    "df['Date'] = df['Date'].dt.strftime('%U')  # %U pour numéro de semaine (dimanche comme premier jour)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "81db0ae7-a29d-492e-944f-cdfe2121179d",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "TCD_EDF_Semaine = df.pivot_table(index=[\"Année\", \"Semaine\"], values=\"Total EDF\", aggfunc=lambda x: round(x.mean(), 1))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "fe77f276-cb79-4614-906d-62f9f6007092",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "def plot_graph(data):\n",
    "\n",
    "    # Créer le graphique\n",
    "    plt.figure(figsize=(8, 5), facecolor='lightgrey')\n",
    "\n",
    "    # Créer une liste de chaînes représentant les semaines au format \"année-semaine\"\n",
    "    x_values = [f\"{semaine}\" for annee, semaine in data.index]\n",
    "\n",
    "    # Tracer la courbe avec les paramètres spécifiques\n",
    "    plt.plot(x_values, data['Total EDF'], linestyle='-', color='r', label='Score EDF moyen', linewidth=2)\n",
    "\n",
    "\n",
    "\n",
    "    # Ajouter un titre, des labels d'axes\n",
    "    plt.title(\"Evolution de l'EDF moyen par semaine sur la saison 2023-2024\", color='black', fontweight='bold', fontsize=12)\n",
    "    plt.xlabel(\"Semaines\", color='black', fontweight='bold')\n",
    "    plt.ylabel(\"Score EDF moyen\", fontweight='bold')\n",
    "\n",
    "    # Définir les limites de l'axe des ordonnées (y-axis)\n",
    "    plt.ylim(10, 30)\n",
    "\n",
    "    # Ajuster les marges pour que le premier point soit aligné avec l'axe des ordonnées\n",
    "    plt.margins(x=0)  # Ajustement horizontal (axe des abscisses)\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "    # Couleur de fond (zone de traçage)\n",
    "    ax = plt.gca()\n",
    "    ax.set_facecolor('beige')\n",
    "\n",
    "    # Couleur sous la courbe\n",
    "    plt.fill_between(x_values, data['Total EDF'], 0, where=(data['Total EDF'] > 0), alpha=0.3, color='blue')\n",
    "\n",
    "\n",
    "\n",
    "    # Afficher la légende\n",
    "    plt.legend(loc='upper right', fontsize='small', title='Légende', facecolor='lightgrey', frameon=True, edgecolor='black', fancybox=True)\n",
    "\n",
    "    # Afficher le graphique\n",
    "    plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "1c90653a-bc7b-45cb-ad1e-09b2776c8be1",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "def update_plot(joueur):\n",
    "    # Filtrer les données en fonction du joueur sélectionné\n",
    "    if joueur == \"Moyenne Groupe\":\n",
    "        filtered_data = df  # Utiliser toutes les données pour la moyenne du groupe\n",
    "    else:\n",
    "        filtered_data = df[df['Nom'] == joueur]  # Filtrer les données pour le joueur sélectionné\n",
    "\n",
    "    # Agréger les données filtrées par semaine et année\n",
    "    TCD_filtered = filtered_data.pivot_table(index=[\"Année\", \"Semaine\"], values=\"Total EDF\", aggfunc=lambda x: round(x.mean(), 1))\n",
    "\n",
    "    # Afficher le graphique mis à jour\n",
    "    plot_graph(TCD_filtered)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c6611ae5-4db2-47a0-80c8-708205c610be",
   "metadata": {},
   "source": [
    "# Evolution groupe/indiv RPE et EDF"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "4516d847-b577-4d6f-9619-b1356fc9d356",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "391101b04b474c5daa49a7f8a0403f36",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "interactive(children=(Dropdown(description='Joueur :', options=('Moyenne Groupe', 'ARRIGHETTI', 'BAGMA', 'BATA…"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/plain": [
       "<function __main__.update_plot(joueur)>"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Liste des joueurs disponibles triée par ordre alphabétique\n",
    "joueurs_disponibles = sorted(df['Nom'].unique().tolist())\n",
    "\n",
    "# Insérer \"Moyenne Groupe\" en haut de la liste\n",
    "joueurs_disponibles.insert(0, \"Moyenne Groupe\")\n",
    "\n",
    "# Sélecteur de joueur\n",
    "joueur_selector = widgets.Dropdown(options=joueurs_disponibles, description='Joueur :')\n",
    "\n",
    "# Connecter le widget à la fonction de mise à jour du graphique\n",
    "widgets.interact(update_plot, joueur=joueur_selector)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "af335f1d-e123-4b19-897d-de1ff83707a2",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
