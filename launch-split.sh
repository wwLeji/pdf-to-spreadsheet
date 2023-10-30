#check if python3 is installed
if ! [ -x "$(command -v python3)" ]; then
  # install python3 if not installed with homebrew
    if ! [ -x "$(command -v brew)" ]; then
        echo 'Error: brew is not installed.' >&2
    else
        brew install python3
    fi
fi

# Obtient le nom d'utilisateur actuel
name=$(whoami)

# Répertoire où se trouve le fichier "$directory/things-to-keep.txt"
directory="/Users/$name/Desktop/pdf-to-excel"

python3 $directory/files/test.py

# Vérifie si le fichier "$directory/things-to-keep.txt" existe
if [ -e "$directory/things-to-keep.txt" ]; then
    # lire la dernière ligne du fichier
    last_line=$(tail -n 1 $directory/things-to-keep.txt)
    echo $last_line
    if [ "$last_line" != "" ]; then
        # ajoute une ligne vide à la fin du fichier
        echo "" >> $directory/things-to-keep.txt
    fi
    # Lit chaque ligne du fichier et exécute le script avec les arguments
    while IFS= read -r line; do
        cd $directory
        python3 $directory/files/split-in-excel.py $line
    done < "$directory/things-to-keep.txt"
else
    echo "Le fichier '$directory/things-to-keep.txt' n'existe pas."
fi

# rm $directory/text.txt