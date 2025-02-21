import cmd
import textwrap
import sys
import os
import time
import random

screen_width = 100

################
# Player Setup #
################


class Player:
    def __init__(self, position=None):
        self.name = ''
        self.feeling = ''
        self.choice = ''
        self.position = position
        self.won = False
        self.inventory = []
        self.solves = 0

	    
player1 = Player()

#############
# Map Setup	#
#############

"""
La forteresse fonctionne sous forme de couloir , pour avancer il y a toujours un choix vers une salle à décider -
Tout commence avec un choix de direction à l'éntrée (gauche) ou (droite) ce qui déterminera la map sur laquelle le joueur se trouvera -
Ensuite , il devra avancer de zone en zone avec un évènement ou plutôt un puzzle , il doit être réussit pour avancer à la prochaine zone -
Une fois les 4 puzzles / zones résolus , il y a qu'une seule direction le BOSS.

----------------------------------------------------


                  [Choix]
              |  |       |  |
------------    <-        ->  ----------------
/   A1 /  B1  /              Z1 / Y1 / X1 / W1 /
-------------                ---------------
/   A2 /  B2  /               / Z2 / Y2 / X2 /
-------------  Map 1         ---------------          Map 2
/  A3  /  B3 /                / Z3 / Y3 / X3 /
-------------               ---------------
             

-------------              ---------------
        -->             <--               
			     |  |
                [BOSS]


-----------------------------------------------------
"""

# map va
DESCRIPTION = 'description'
INFO = 'info'
PUZZLE = 'puzzle'
SOLVED = 'solved'
CONTINUE = 'continue'
OPTION = 'option'



check_points = {'ENTREE': False,'A1': False, 'B1': False, 'A2': False, 'B2': False, 'A3': False, 'B3': False,'BOSS': False}


map1 = {
       'ENTREE': {
        DESCRIPTION: "Après dix jours de marche intense , vous vous retrouver face à cette immense forteresse.Sa structure imposante vous laisse perplexe à l'idée d'entrer mais vous n'avez pas fait tout ce chemin pour rien !(inspecter)",
        INFO: "Une fois à l'intérieur vous êtes directemenet confronter à deux couloirs menant à des portes , comment une telle disposition est-elle possible ? ",
        PUZZLE: "Votre coeur palpite à l'idée de choisir , bien que l'endroit ne comporte qu'une seule résidente , elle pourrait vous prendre par surprise à tout moment.Il vous faut faire un choix (droite)/(gauche)",
        SOLVED: ['droite', 'gauche'],
        'OPTION': {
               'gauche': "Une porte tout à fait normal s'impose devant cependant vous n'arrivez pas à l'ouvrir , il va falloir y mettre un peu plus de force.",
               'droite': "Une arachnide vous observe et semble enthousiaste à l'idée vous voir , elle marque un certain intérêt pour un chemin.",
        },
        CONTINUE: ['A1', 'B1'],

    },
    'A1': {
        DESCRIPTION: "Vous foncez droit comme une flèche sur la porte.Vous sentez comme la forte odeur d'un délicieux plat, impossible d'y résister vous la suivez.Votre intuition était juste : il s'agissait bien d'une cuisine. (inspecter)",
        INFO: "Vous observez les alentours à la recherche de signes de vie, mais rien. Seule une marmite semble contenir le ragoût de viande le plus alléchant du monde après des jours sans manger vous avez tout même le droit à un repas , non ?",
        PUZZLE: "Vous attrapez le premier ustensile qui vous permettrait de vous goinfrer, et c'est alors qu'un rat émerge de la sauce contenue dans la marmite. Il ne semble pas d'accord pour partager avec vous ce délicieux repas. Que faites-vous ? (enfoncer)/(sortir)",
        SOLVED: ['enfoncer', 'sortir'],
        'OPTION': {
               'enfoncer': "Arme à la main , vous frapper la tête de la bestiole pour la noyer dans la sauce , quelques secondes après elle resurgit.. puis maintenant elles sont deux puis 3 ça ne s'arrête pas.La scène vous écoeure au plus au point vous qui était prêt à ingurgeter ce plat , vous quitter la pièce.",
               'sortir': "Ustensile à la main vous le positionner délicatement dessus pour sortir le rat , il semble pacifiste et vous laisse faire sans encombre.Alors que vous vous offrez le plus grand met de votre vie , il vous regarde d'un air atristé après tout il était la avant vous.Vous lui offrez un bol de délicieux plat avant de reprendre votre route.",
        },
        CONTINUE: ['A2', 'B2'],
    },
    'B1': {
        DESCRIPTION: "Vous suivez une arachnide et vous vous retrouvez dans la bibliothèque, avec de nombreuses étagères remplies de livres.(inspecter)",
        INFO: "Tout au fond de la pièce, vous arrivez à discerner un objet brillant de couleur rougeâtre. Il est clairement exposé à la vue de tous, comme pour inciter à aller voir ce qui s'y trouve.",
        PUZZLE: "Vous grimpez l'échelle qui mène à cette intriguante étagère. Vous vous retrouvez face à l'objet brillant, qui est en réalité un parchemin magique. Vous savez que pour l'utiliser, il suffit de lire la formule, mais vous êtes dans l'incapacité de déchiffrer le fonctionnement du sort. Que faites-vous ? (prendre)/(partir)",
        SOLVED: ['prendre', 'partir'],
        'OPTION': {
               'prendre': "Le parchemin a peut être une grande valeur , une chance pour vous il y a asssez de place dans votre sac.Vous continuez votre route.",
               'droite': "Les objets magiques et vous ce n'est pas un grande histoire d'amour , vous ne laisserez pas la cupidité vous tuer aujourd'hui.",
        },
        CONTINUE: ['A2', 'B2'],
    },
    'BOSS': {
        DESCRIPTION: "La dernière porte de cette infâme forteresse. Il est temps pour vous de mettre fin à cette aventure : battre la voleuse, récupérer ce pourquoi vous êtes venu et rentrer. À la seconde où vous franchissez le seuil de la pièce, vous vous rendez compte que vous êtes sur le toit. Mais plus important encore, le ciel et la pluie sont d'un rouge sang aussi étrange qu'inquiétant. (inspecter)",
        INFO: "La peur vous envahit quand soudain, des bruits dans votre dos vous incitent à vous retourner. Vous vous retrouvez face à une silhouette féminine... Vous en déduisez qu'il s'agit de votre cible. La montre, qui jusque-là n'émettait que de la lumière, commence à vibrer intensément à mesure que la silhouette s'approche. La lumière s'intensifie, puis l'appareil explose, vous submergeant d'une lumière aveuglante. Vous ne voyez plus rien pendant quelques instants. En ouvrant les yeux, vous réalisez que vous n'êtes plus sur le toit. Vous avez changé de pièce, ou plutôt, c'est la pièce elle-même qui a changé.",
        PUZZLE: "La silhouette qui était jusque-là féminine commence lentement à se transformer. Ses traits se distordent, son corps se fait plus large, ses mouvements moins raffinés. Les courbes se gonflent, l'apparence devient grossière et déformée, et ses gestes prennent une lourdeur maladroite. La finesse cède place à une silhouette plus vulgaire, presque caricaturale, avec un air dédaigneux. Cette apparence ne vous est pas inconnue. Vous en avez déjà entendu parler dans les livres de la Guilde : une créature incarnant la malveillance et la cruauté à son paroxysme... c'est une GUENAUDE ! L'elfe n'avait pas précisé ce détail , comment sortir de cette situation en vie ? L'objet était-ce elle ? Tout ceci était un piège ? (combattre)/(fuir)",
        SOLVED: ['combattre','fuir'],
        'OPTION': {
               'combattre': "Vous charger sur la créature , poussant un cri de rage , vous élancer votre poing avec toute votre volonté.Avant même d'avoir pu faire 10 pas , elle se téléporte vous poignarde en plein coeur , vos forces vous quittent.. et la partie se termine ici. (quitter)",
               'fuir': "Impossible de battre une telle créature , au diable l'elfe et sa fichue quête.Vous n'êtes pas le héros de cette histoire , juste un survivant.Vous prenez vos jambes à votre cou , avant même même d'avoir pu faire 10 pas , elle se téléporte vous poignarde en plein coeur , vos forces vous quittent.. et la partie se termine ici. (quitter)",
        },
        
        CONTINUE: ['A3'],
    },
    'A2': {
        DESCRIPTION: "Vous vous dirigez vers le bruit mécanique que vous avez entendu. La pièce semble faire office de cave, mais vous n'êtes pas descendu au niveau inférieur. Vous continuez votre route. (inspecter)",
        INFO: "Alors que vous continuez votre traversée, vous remarquez qu'il y a un problème. Vous avez l'impression que le sol se dérobe sous vos pieds, comme si la pièce changeait de forme autour de vous. L'air semble lourd, comme si la gravité elle-même était manipulée par une force invisible. Vous vous retrouvez soudainement dans une version différente de la salle, comme si un étage entier venait d'apparaître sous vos yeux.",
        PUZZLE: "Comme à son habitude, l'entrée par laquelle vous êtes passé semble bloquée. Vous continuez d'avancer ? (avancer)",
        SOLVED: ['avancer'],
        'OPTION': {
               'avancer': "La pièce commence à devenir instable , elle tremble de toute part.Il est temps pour vous de vous en aller. ",
        },
        CONTINUE: ['A3', 'B3'],
    },
    'B2': {
        DESCRIPTION: "Vous passez la porte de la salle, mais vous ne voyez aucune lumière, simplement l'obscurité. L'idée de continuer vous terrifie, mais vous devez le faire. (inspecter)",
        INFO: "À mesure que vous continuez votre périple dans la pièce, vous sentez un regard persistant sur vous. Mais comment cela peut-il être possible ? Vous êtes seul dans l'obscurité... ou pas.",
        PUZZLE: "Vous avez beau essayer de garder votre calme, la situation est bien trop pesante. Vous devez faire quelque chose ! (courir)/(faire face)",
        SOLVED: ['faire face', 'courir'],
        'OPTION': {
               'faire face': "Un héros doit se montrer courageux ! Vous vous retourner et faîtes face à.. un crâne de squelette , ses yeux sont ornés de diamants.Le dialogue ne semble pas possible cependant il est complètement docile malgré son regard insistant sur vous.Vous le ranger dans votre sac.",
               'courir': "La fuite est parfois la meilleure solution , vous ne voulez pas savoir ce qui vous attend si vous vous retourner.Vous courez à tout vas pour sortir de cette pièce",
        },
        CONTINUE: ['A3', 'B3'],
    },
    'A3': {
        DESCRIPTION: "Vous entrez dans la pièce et, dès votre entrée, vous êtes stupéfait par l'endroit. Il s'agit de la salle à manger. Tout semble en parfait état pour accueillir un invité... peut-être vous ? (inspecter)",
        INFO: "Sur les murs de la pièce, vous observez deux tableaux. Vous n'arrivez pas à y croire. Le premier représente votre silhouette ensanglantée dans un volcan en fusion sur une montagne de cadavres... des orcs par centaines. Vous brandissez votre épée vers le ciel en signe de victoire. Vous semblez HÉROÏQUE. Le deuxième tableau représente à nouveau votre silhouette, mais cette fois, vous êtes sur un trône, couronne à la tête, bagues aux doigts, entouré de montagnes de pièces d'or. Vous semblez PUISSANT.",
        PUZZLE: "Alors que vous cherchez à comprendre comment et pourquoi votre vie n'est pas aussi géniale qu'elle est représentée sur les tableaux, quelque chose se passe. Les deux silhouettes commencent à bouger dans votre direction. L'une tend une épée, peut-être la plus belle que vous ayez jamais vue, l'autre tient un minerai d'adamantium. Il n'y a rien de plus rare en terme de minerai dans ces contrées. Que prenez-vous ? (épée)/(minerai)",
        SOLVED: ['épée', 'minerai'],
        'OPTION': {
               'épée': "L'épée est scintillante , elle est un état parfait comme si elle sortait toute juste la meilleur des forges façon par le meilleur des forgerons.Votre gabarit n'est pas du tout taillé pour utiliser cette épée , vous pourrez en tirer un prix la vente.Vous la passer à votre taille et continuer votre route.",
               'minerai': "Pas de doute possible , il s'agit bien d'adamantium.Sa taille est suffisante en faire un bijoux , vous vous ferez remarquer à coup sûr.Vous le ranger dans votre sac et passer à la suite du chemin.",
        },
        CONTINUE: ['BOSS'],
    },
    'B3': {
        DESCRIPTION: "Vous entrez dans la pièce et vous vous apercevez que ce n'en est pas vraiment une, mais un autre couloir. Des étranges caisses sont disposées tout le long jusqu'à la porte de sortie au fond. (inspecter)",
        INFO: "Votre curiosité vous pousse à jeter un coup d'œil à l'intérieur des caisses. La plupart semblent vides, mais d'autres contiennent d'étranges masques en bois. En inspectant de plus près l'un d'eux, il semble dégager un sinistre murmure. Vous n'arrivez pas à discerner clairement ce qui est dit.",
        PUZZLE: "Le choix vous revient. Vous ne savez pas quelle importance ils ont, mais peut-être pourrez-vous en tirer une quelconque utilité. Que faites-vous ? (prendre)/(détruire)",
        SOLVED: ['prendre', 'détruire'],
        'OPTION': {
               'prendre': "Un objet maléfique c'est toujours bon la vente , vous l'accrocher à votre ceinture et passer votre chemin.",
               'détruire': "Vous ne chercher pas à comprendre le maléfice que ce masque , vous le laisser tomber au sol puis frapper d'un coup vertcial dessus avec votre pied pour le briser.Les murmures s'arrêtent..rien d'autre ne se passe , vous déchainez la colère et le stresse parcouru dans la forteresse sur les masques et continuer votre chemin.",
        },
        CONTINUE: ['BOSS'],
    }
}


################
# Title Screen #
################

def title_screen_options():
    
    option = input("> ").strip()
    while option.lower() not in ['jouer', 'commandes', 'quitter']:
        print("Oulah, mauvaise commande. Essayez 'Jouer', 'Commandes' ou 'Quitter'.")
        option = input("> ").strip()
    
    if option.lower() == "jouer":
        setup_game()
    elif option.lower() == "quitter":
        sys.exit()
    elif option.lower() == "commandes":
        help_menu()

def title_screen():
    
    os.system('cls')  
    
    print('_=_' * 15)
    print('#       ~ La forteresse de Beverstone ~    #')
    print('-~' * 23)
    print("#      William Agossah - Projet Python     #")
    print('_=_' * 15)
    print("                  .: Jouer :.                  ")
    print("                .: Commandes :.                  ")
    print("                 .: Quitter :.                  ")
    title_screen_options()


#############
# Help Menu #
#############

def help_menu():
	print("")
	print('#' * 45)
	print("En arrivant dans une salle écrire INSPECTER pour déclencher une interraction\n")
	print("Pour choisir une salle faire DROITE ou GAUCHE.\n")
	print('#' * 45)
	print("\n")
	print('#' * 45)
	print("                     Menu                       ")
	print('#' * 45)
	print("                 .: Jouer :.                  ")
	print("               .: Commandes :.                  ")
	print("                .: Quitter :.                  ")
	title_screen_options()
	
#################
# Game Handling #
#################
quitgame = 'quit'

# Fonction pour afficher la description de la pièce où se trouve le joueur
def print_location():
    print('\n' + ('#' * (4 + len(player1.position)) ))
    print('# ' + player1.position.upper() + ' #')
    print('#' * (4 + len(player1.position)))
    print('\n' + (map1[player1.position][DESCRIPTION]))


def show_inventory():
    if player1.inventory:
        print("\nVotre inventaire :")
        for item in player1.inventory:
            print(f"- {item}")
    else:
        print("\nVotre inventaire est vide.")

#afficher prompt 
def prompt():
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~")
    slow_print("Choisir une action")
    action = input("> ").lower()
    
    acceptable_actions = ['inspecter', 'quitter', 'gauche', 'droite', 'inventaire']  
    
    while action not in acceptable_actions:
        print("Commande inconnue, veuillez réessayer.\n")
        action = input("> ").lower()
    
    if action == 'quitter':
        sys.exit("Le jeu est terminé. Merci d'avoir joué !")
    elif action in ['gauche', 'droite']:
        move(action)
    elif action == 'inspecter':
        inspecter()  
    elif action == 'inventaire':
        show_inventory()  

#
def move(myAction):
    if check_points[player1.position] == False:
        print("Vous devez d'abord inspecter la salle avant de partir.")
        return

    if player1.position in ['A3', 'B3']:
        player1.position = 'BOSS'
        print_location()
    else:
        if myAction == 'gauche':
            move_dest = map1[player1.position][CONTINUE][0]
        elif myAction == 'droite':
            move_dest = map1[player1.position][CONTINUE][1]

        if move_dest:
            print(f"\nVous vous déplacez vers la salle {move_dest}.")
            player1.position = move_dest
            print_location()
        else:
            print("Désolé, vous ne pouvez pas vous déplacer dans cette direction.")


def move_player(move_dest):
    if move_dest:
        print("\nVous vous êtes déplacé vers " + move_dest + ".")
        player1.position = move_dest
        print_location()
    else:
        print("Désolé, vous ne pouvez pas vous déplacer dans cette direction.")


def inspecter():

    if check_points[player1.position] == False:
       
        print('\n' + (map1[player1.position].get(INFO, "Aucune information disponible.")))
        print((map1[player1.position].get(PUZZLE, "Aucun puzzle défini.")))

        puzzle_answer = input("> ").lower().strip()


        if puzzle_answer in map1[player1.position].get(SOLVED, []):
            #ffiche le dialogue associé
            if puzzle_answer in map1[player1.position].get('OPTION', {}):
                slow_print(map1[player1.position]['OPTION'][puzzle_answer])
            else:
                print("Aucun dialogue spécifique trouvé pour ce choix.")

            #Marque la salle comme résolue
            check_points[player1.position] = True
            print("Vous pouvez maintenant continuer d'explorer.")
        else:
            print("Réponse invalide. Essayez encore.")
            return
    else:
        print("Il n'y a rien de nouveau à examiner ici.")





def main_game_loop():
	total_puzzles = 6
	while player1.won is False:
		prompt()



################
# Execute Game #
################

def setup_game():
	os.system('cls')

	
	question1 = "Tout aventurier à besoin d'un nom , c'est quoi le tien ?\n"
	for character in question1:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
	player_name = input("> ")
	player1.name = player_name

	
	question2 = " Alors " + player1.name + ", tu te sens comment ?\n"
	for character in question2:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
	feeling = input("> ")
	player1.feeling = feeling.lower()

	


good_adj = [
    'bon', 'super', 'rohit', 'heureux', 'bien', 'compréhensif', 'super', 
    'd’accord', 'calme', 'confiant', 'pas mal', 'courageux', 'paisible', 
    'fiable', 'joyeux', 'énergique', 'à l\'aise', 'facile', 'chanceux', 'k', 
    'confortable', 'étonné', 'fortuné', 'optimiste', 'content', 'libre', 
    'ravi', 'heureux', 'encouragé', 'ok', 'enchanté', 'impulsif', 'malin', 
    'intéressé', 'joyeux', 'libre', 'surpris', 'satisfait', 'reconnaissant', 
    'vif', 'content', 'réceptif', 'important', 'animé', 'silencieux', 'd’accord', 
    'festif', 'plein d\'esprit', 'certain', 'gentil', 'électrisé', 'exalté', 
    'détendu', 'satisfait', 'merveilleux', 'serein', 'content', 'libre', 'et', 
    'facile', 'joyeux', 'brillant', 'ensoleillé', 'béni', 'joyeux', 'rassuré', 
    'exalté', '1738', 'amour', 'intéressé', 'positif', 'fort', 'aimant'
]

hmm_adj = [
    'je sais pas', 'préoccupé', 'lakshya', 'avide', 'impulsif', 'considéré', 
    'affecté', 'désireux', 'libre', 'affectueux', 'fasciné', 'sincère', 'sûr', 
    'sensible', 'intrigué', 'intéressé', 'certain', 'tendre', 'absorbé', 'anxieux', 
    'rebelle', 'dévoué', 'curieux', 'inspiré', 'unique', 'attiré', 'curieux', 
    'déterminé', 'dynamique', 'passionné', 'fouineur', 'excité', 'tenace', 
    'admiration', 'absorbé', 'enthousiaste', 'endurant', 'chaleureux', 'curieux', 
    'audacieux', 'sûr', 'touché', 'brave', 'sympathie', 'audacieux', 'proche', 
    'défié', 'aimé', 'optimiste', 'réconforté', 're', 'renforcé', 'attiré', 
    'vers', 'confiant', 'plein d\'espoir', 'difficile'
]

bad_adj = [
    'mauvais', 'bof', 'triste', 'affamé', 'désagréable', 'sentiments', 'en colère', 
    'déprimé', 'confus', 'impuissant', 'irrité', 'nul', 'upset', 'incapable', 'enragé', 
    'déçu', 'douteux', 'seul', 'hostile', 'découragé', 'incertain', 'paralysé', 
    'insultant', 'honteux', 'indécis', 'fatigué', 'douloureux', 'nul', 'perplexe', 
    'inutile', 'agaçant', 'diminué', 'embarrassé', 'inférieur', 'upset', 'coupable', 
    'hésitant', 'vulnérable', 'horrible', 'insatisfait', 'timide', 'vide', 
    'désagréable', 'misérable', 'stupeur', 'forcé', 'offensif', 'détestable', 
    'désillusionné', 'hésitant', 'amer', 'répugnant', 'incrédule', 'désespoir', 
    'agressif', 'méprisable', 'sceptique', 'frustré', 'ressentiment', 'dégoûtant', 
    'méfiant', 'détressé', 'enflammé', 'abominable', 'doute', 'navrant', 'provoqué', 
    'terrible', 'perdu', 'pathétique', 'enragé', 'en', 'désespoir', 'incertain', 
    'tragique', 'exaspéré', 'boudeur', 'anxieux', 'en colère', 'mauvais', 'pessimiste', 
    'dominé', 'épuisé', 'un', 'sens', 'de', 'perte', 'tendu', 'bouillant', 'fumant', 
    'indigné', 'indifférent', 'effrayé', 'blessé', 'triste', 'insensible', 'peureux', 
    'écrasé', 'en larmes', 'terne', 'terrifié', 'tourmenté', 'attristé', 'nonchalant', 
    'méfiant', 'privé', 'douleur', 'neutre', 'anxieux', 'douleur', 'tristesse', 'réservé', 
    'malheureux', 'torturé', 'angoisse', 'fatigué', 'panique', 'abattu', 'désolé', 'ennuyé', 
    'nervosé', 'rejeté', 'désespéré', 'préoccupé', 'effrayé', 'blessé', 'pessimiste', 
    'froid', 'inquiet', 'offensé', 'malheureux', 'désintéressé', 'effrayé', 'affligé', 
    'solitaire', 'sans vie', 'timide', 'douloureux', 'attristé', 'tremblant', 'victimisé', 
    'triste', 'inquiet', 'déçu', 'douteux', 'angoissé', 'menacé', 'écoeuré', 'lâche', 
    'humilié', 'tremblant', 'injustement traité', 'menacé', 'aliené', 'prudent'
]


	
	
if player1.feeling in good_adj:
		feeling_string = "C'est super alors !"
elif player1.feeling in hmm_adj:
		feeling_string = "C'est pas bon signe , je suppose.."
elif player1.feeling in bad_adj:
		feeling_string = "Navré d'entendre ça."
else:
		feeling_string = "Je suis une machine , je ne connais pas ce sentiment"

	
question3 = "Eh bien, " + player1.name + ", " + feeling_string + " " + player1.feeling + ".\n"
for character in question3:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)

	
question4 = "J'aimerais que tu fasses un choix \n"
for character in question4:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)

	# Question pour le BOSS aprè
print("#####################################################")
print("# Choisis un numéro dans cette liste :")

print("# 1. 🦸‍♀️💥 Avengers : Infinity War")
print("# 2. 🚢❄️ Titanic")
print("# 3. 🦁👑 Le Roi Lion")
print("# 4. 🌹🎨 Georges Rochegrosse")
print("# 5. ⚔️🐺 The Witcher 3: Wild Hunt")
print("# 6. 💼🖨️🤣 The Office")
print("# 7. ☕👫 Friends")
print("# 8. 🥋🌀 Street Fighter")
print("# 9. 🐱💎 Pokémon")
print("# 10. ⚡💣 Overwatch")
print("# 11. 🏰🧙‍♂️✨ Baldur's Gate 3")
print("# 12. ⚔️💀 Dark Souls ")
print("# 13. Pourquoi je devrais faire ça  ?")
print("#####################################################")


choice = input("Entrez un numéro : ")


choices = {
    '1': 'Avengers : Infinity War',
    '2': 'Titanic',
    '3': 'Le Roi Lion',
    '4': 'Georges Rochegrosse',
    '5': 'The Witcher 3: Wild Hunt',
    '6': 'The Office',
    '7': 'Friends',
    '8': 'Street Fighter',
    '9': 'Pokémon',
    '10': 'Overwatch',
    '11': 'Baldur\'s Gate 3',
    '12': 'Dark Souls',
	'13': 'Pourquoi je devrais faire ça'
}


if choice in choices:
    print(f"Tu as choisis : {choices[choice]}")
else:
    print("Mauvais choix.")

	
speech1 = "Oh , un choix , intéressant..\n"
speech2 = "Bien , il est temps de partir " + player1.name + ".\n"
speech3 = "Que la force ou la chance soit avec toi.\n"  
speech4 = "Tâche de revenir en vie.\n"
speech5 = "Pourquoi je dis ça ? Moi-même , je ne sais pas ce qui t'attends mais ce sera sûrement dangereux.\n"
speech6 = "...\n"
for character in speech1:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
for character in speech2:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
for character in speech3:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.1)
for character in speech4:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
for character in speech5:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
for character in speech6:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.2)
time.sleep(1)

os.system('cls')

def slow_print(text, delay=0.05):
    """Affiche le texte caractère par caractère avec un délai entre chaque caractère."""
    for char in text:
        print(char, end='', flush=True)  # Affiche chaque caractère sans nouvelle ligne
        time.sleep(delay)  # Pause entre chaque caractère
    print()  # Une fois que tout le texte est imprimé, on passe à la ligne suivante
	
slow_print("À la recherche d'une quête pouvant vous permettre de gravir les échelons, personne ne semble croire en vos compétences et on vous assigne une mission..\n")
slow_print("Déprimé par cette journée, vous sortez du bâtiment de la Guilde, vous remettez en cause votre avenir dans cette profession quand soudain, un elfe s'interpose entre vous et le chemin de la déprime.\n")
slow_print("...\n")
slow_print("L'elfe, vêtu d'une robe de voyage usée mais élégante, prend la parole d'une voix douce mais ferme :\n")
slow_print("\"Je vois dans tes yeux que le doute te ronge, jeune aventurier. Mais ne laisse pas cette déception t'éteindre. La vie n'est pas faite de simples victoires... mais de défis qui façonnent notre véritable potentiel.\"\n")
slow_print("Il se tait un instant, et vous sentez une étrange énergie émaner de lui. Puis, il ajoute :\n")
slow_print("\"Je suis en quête de quelqu'un de spécial. Une mission bien plus importante que celle de la Guilde. Peut-être que tu es celui que je cherche... ou peut-être pas.\"\n")
slow_print("Un sourire énigmatique flotte sur ses lèvres. Vous ressentez quelque chose d'étrange autour de cet elfe, puis un pressentiment vous traverse l'esprit, comme si cette rencontre marquait le début d'un grand événement pour vous.\n")
slow_print("Il vous explique qu'il est à la recherche de quelqu'un d'assez courageux pour se rendre à la Forteresse de Beverstone, un vestige du passé, abandonné depuis des siècles, et désormais le repaire d'une voleuse qui détient un objet d'une grande importance.\n")
slow_print("Il vous tend un objet : une montre de poche, imprégnée de magie. En vous rendant dans la forteresse pour retrouver son précieux, la montre émettra une lumière rosée dès que vous serez suffisamment proche de l'objet.\n")
slow_print("Personne n'est assez fou pour entreprendre une telle expédition tête baissée à la demande d'un inconnu, et pourtant, vous, et votre ego, semblez croire que tout vous est possible.\n")
slow_print("En avant Monsieur le Héros..")

player1.position = 'ENTREE'
print_location()  


	

main_game_loop()


title_screen()
