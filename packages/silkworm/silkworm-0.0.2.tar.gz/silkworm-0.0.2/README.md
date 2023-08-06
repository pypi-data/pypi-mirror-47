# SILKWORM

## What is SILKWORM?
**S**tandard
**I**ntegrated
**L**ibraries
**K**ey for
**W**orking
**O**n
**R**esearch at
**M**ESH

## What's in each branch?
| Branch			| Description															                           |
| ------------ | --------------------------------------------------------------------------------- |
| master       | Tested, fully working, fully integrated, and reviewed by 2 people.                |
| develop		| Tested, fully working, not integrated. Reviewed by comitters.                     | 
| rothtime     | rothtime package                                                                  |

Branches that aren't master or develop are dedicated to packages. Large packages may have multiple branches and follow the convention `package/feature`

## Currently Available Packages
* [rothtime](silkworm/rothtime)
	Standard utilties for high fidelity timing.

## How Do I Use SILKWORM in My Project?

Currently there is no way to install SILKWORM as a pip package. This is being worked on.

### Adding silkworm to your project
To use SILKWORM, you currently have 2 optoins detailed below.
- Clone SILKWORM and dump the silkworm package into your project.
```shell
git clone https://github.iu.edu/emchow/SILKWORM.git
cp -R SILKWORM/silkworm path/to/project/silkworm/folder
```

- Add SILKWORM as a git submodule. **(Recommended)**

```shell
cd /path/to/project/folder
git submodule add https://github.iu.edu/emchow/SILKWORM.git 
git commit -m "Added SILKWORM to my project"
```

### Managing SILKWORM in a project
Adding SILKWORM as a submodule allows you to recieve updates without recloning. There are two ways to recieve updates: 
	
- You may use `git fetch` within the subdirectory your submodule resides in
- Use `git submodule update --remote` somewhere in your git project's directory (not inside of a submodule). This will update all submodules. **(Recommended)**



To clone such projects, and their submodules use `git clone --recurse-submodules` 

It is recommended to keep all branches with a copy of SILKWORM if you do this. Not doing so will cause issues when switching branches.

You can read more about git submodules [here](https://git-scm.com/book/en/v2/Git-Tools-Submodules)

**Note to Contributors**: I do not recommend you edit SILKWORM from the submodule unless absolutely necessary. Merge conflicts can be difficult to resolve in your project
if they occur. Also there is a high chance of causing future merge conflicts from whatever package you edited to develop.


