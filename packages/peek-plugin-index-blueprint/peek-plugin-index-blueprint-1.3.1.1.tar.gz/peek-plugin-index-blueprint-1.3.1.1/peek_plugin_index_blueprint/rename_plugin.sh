#!/usr/bin/env bash


# remove the git index
#[ -f .git/index ] && rm .git/index || true

#rm -rf dist *egg-info || true

find ./ -name '__pycache__' -exec rm -rf {} \; || true


set nounset
set errexit

function replace {
    from=$1
    to=$2

    for d in `find ./ -depth -type d`
    do
        new=`echo $d | sed "s/$from/$to/g"`
        [ "$d" != "$new" ] && mv $d $new
    done

    for f in `find ./ -type f`
    do
        new=`echo $f | sed "s/$from/$to/g"`
        [ "$f" != "$new" ] && mv $f $new
    done

    for f in `find ./ -type f -not -name '.git' -not -name 'rename_plugin.sh'`
    do
        sed -i "s/$from/$to/g" $f
    done

}



## RENAME THE PLUGIN
#replace "_index_blueprint" "_graphdb"
#replace "-index-blueprint" "-graphdb"
#
#replace "IndexBlueprint" "GraphDb"
#replace "indexBlueprint" "graphDb"
#
#replace "_INDEX_BLUEPRINT" "_GRAPHDB"
#replace "-INDEX-BLUEPRINT" "-GRAPHDB"


## RENAME THE INDEX CLASSES
#replace "_thing"  "_item"
#replace "-thing" "-item"
#
#replace "_THING" "_ITEM"
#replace "-THING" "-ITEM"
#
#replace "Thing" "Item"
#replace "thing" "item"



# Remove compile generated javascript
find ./ -type f -not -name '.git' -name "*.js" -exec rm {} \; || true
find ./ -type f -not -name '.git' -name "*.js.map" -exec rm {} \; || true
