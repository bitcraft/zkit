zkit asset manager
==================


## rationale

To make known and remove all bike shedding traps when dealing with file organization.

Large projects with many contributors will develop warring states on the repo tree,
where each contributor imposes their systems of file naming and filing into folders onto
neighboring others.  This provides no end of merge conflicts and cross-platform issues
which are dealt with every time new assets come in or are modified.

This conflit exists as a natural state of any project that cannot use 'soft' policy, such
as stern contributor guidelines, or a strongly worded rubric of practices to follow.  This
end less and subtle in-fighting of personal habits around what things should be called,
and where they should be stored is a hidden strain on projects where contributors are
many, and there isn't enough playground police around to make sure everyone follows the
project guidelines.

The zkit asset manager, as envision solely in my own madness, aims to find any possible
avenue for deviation and eliminate it completely.  Its in the interest of self-
preservation that a large project enact technical 'hard' restrictions that limit all
the various, arbitrary means for filing digital content.

This is one such idea.

## all files are unique snowflakes

...and will be given unique names.  Conformity in labels will not be tolerated.  All files
will be assigned a UUID as their filename only.  Any reasonable operating system will
inspect the file and generate an appropriate preview.  File extensions are allowed.
All filenames, including extension will be lower case.

## no folder hierarchies

Flat-earthers will appreciate that their insane world view is validated here.  No deep
nesting of folders except when the number of files in the root presents a strain on the
underlaying filesystem, slowing file access down.  Should it be needed, a new folder
will be added to the root to hold assets.  The folder name will be essentially random.

## check-in

All game assets which are deemed worthy of inclusion must be `checked-in` into the
project asset stores.  Their old identity will be stripped away and forgotten.  Their
new identities will be assigned and the file will be moved into the asset storage
folder with the rest.

## violations and detractors

No exceptions.

## tags

To satisfy those who are comforted by arbitrary labels, a simple "tag" system can be
enabled.  Assets can have tags assigned to them, in order for project maintainers to
identify or find specific things.  Tags are for maintenance only, and there will not
be an API exposed to the game engine, because you know there will be some person
out there who feels a little rebellious and will tag assets in their specific way,
then waste cpu time by searching for them by keyword at runtime.
Hyphens in tags are not allowed.

## code use

It should be mentioned that UUIDs once assigned, cannot be changed.  Changing the UUID
will break game code and content such as maps or 3d models which reference other files.
We do not break game code.  If you are updating an asset, overwrite the previous
version with the new copy.  In code, only UUIDs are allowed.  Any code which uses cute
or clever methods to use tags will be rejected, because clever lookups are another way
to impose arbitrary labeling systems on game assets.

## tags, revisited

There is one possible (POSSIBLE) exception to the UUID-as-filename rule, and that is
allowing tags to be embedded in the filename.  Tags would be hyphen separated.  Some
operating systems do not like long file names, so they will be limited to 255 total
characters.  Tags will follow the UUID.  The game asset loader will only read the UUID
and file extension (maybe) so tags can be assigned, but the game will not break if tags
change.

## code api

The relieve the programmer of undo stress around loading and using game assets, the
zkit asset manager will provide a simple interface to load content in a way that the
programmer only needs to know the UUID and their use.  For example, game assets may be
JPG, PNG, OGG, WAV, etc, but it doesn't matter.  If you know the UUID, when asking for
an object, the object will be loaded from disk and returned as a useful object.  The
API will allow the object type to be manually specified, if needed. 