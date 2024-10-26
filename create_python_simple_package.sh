fill_pyproject () {
    folder_name_="$1" ;
    python_version_="$2" ;
    author_name_="$3" ;
    author_email_="$4" ;
    awk -v FOLDER_NAME="$folder_name_" \
    -v PYTHON_VERSION="$python_version_" \
    -v AUTHOR_NAME="$author_name_" \
    -v AUTHOR_EMAIL="$author_email_" '{
        gsub("PACKAGE_NAME", FOLDER_NAME);
        gsub("PYTHON_VERSION", PYTHON_VERSION);
        gsub("AUTHOR_NAME", AUTHOR_NAME);
        gsub("AUTHOR_EMAIL", AUTHOR_EMAIL);
        print;
    }' "pyproject.toml" > "pyproject.toml.temp" ;
    mv "pyproject.toml.temp" "pyproject.toml" ;
}

closing_message () {
    FOLDER_NAME="$1" ;
    echo "INFO: Done and ready.";
    echo "INFO: Package creation exited successfully." ;
    echo "INFO: The virtual environment has been deactivated for now. Reactivate it to start working." ;
    echo "" ;
    echo "Next steps:" ;
    echo "1. Building the package before uploading: 'python -m build' (from \"$FOLDER_NAME\")." ;
    echo "2. Upload the package to pypi: 'python -m twine upload --repository {pypi|testpypi} dist/*'" ;
    echo "3. Install the package from pypi: 'python -m pip install --index-url {https://test.pypi.org/simple|https://pypi.org/simple} --no-deps $FOLDER_NAME'" ;
    echo "4. If any dependencies are required, edit the \`pyproject.toml\` file, \"\[project\]\" field, and add a \`dependencies\` key with a \`List\[str\]\` value, where each string is a \`pip\`-readable dependency." ;
}

get_origin () {
    arg1="$1" ;
    origin=`realpath $arg1 | awk '{gsub("/[^/]+$", ""); print $0"/"}'` ;
    echo $origin ;
}

origin=$(get_origin "$0");

echo "INFO: Origin folder set to \""$origin"\"." ;
echo "WARNING: Python, pip, and virtualenv are **assumed** to be available locally." ;

echo "Enter folder name for the package:" ;
read folder_name_ ;

echo "Enter package parent folder (if other than '.'):" ;
read folder_parent_ ;
folder_parent__=$(echo "$folder_parent_" | awk '{
    if ($0 !~ "[a-z]") {
        print "./"
    } else {
        if ($0 !~ /\/$/) {
            print $0"/"
        } else {
            print $0
        }
    }
}') ;
folder_parent_=$(realpath $folder_parent__)"/" ;

echo "Initialize as a git repository, too? (\"y\"|\"n\")" ;
read as_repo ;

echo "Enter Python version for the virtual environment:" ;
read python_version_ ;

echo "Enter package author name:"
read author_name_ ;

echo "Enter package author email address:"
read author_email_ ;

if [ ! "$python_version_" ] ; then echo "FATAL: A Python version is required, aborting..." ; exit 1 ; fi;
if [ ! "$folder_name_" ] ; then echo "FATAL: A package folder name is required, aborting..." ; exit 1 ; fi;
if [ ! "$author_name_" ] ; then echo "FATAL: A package author name is required, aborting..." ; exit 1 ; fi;
if [ ! -d "$folder_parent_" ] ; then echo "FATAL: The specified parent folder was not found, please specify an existing folder as the parent folder, aborting..." ; exit 1 ; fi ;
if [ -d "$folder_parent_""$folder_name_" ] ; then echo "FATAL: Objects already exist at the user-specified destination folder, aborting..." ; exit 1 ; fi ;


cd "$folder_parent_" ;

if ! virtualenv -p "$python_version_" "$folder_name_" ; then
    echo "FATAL: Virtual environment creation failed."
    exit 1 ;
fi ;

cd "$folder_name_" ;
work_folder=$(pwd);
echo "INFO: Setting \""$work_folder"\" as the work folder and changing into it..."

source bin/activate ;
echo "DONE: Virtual environment activated." ;

if [ "$as_repo" = "y" ] ;
    then git init ;
    echo "DONE: Initialized empty repository at \"$folder_name_\".";
fi ;

echo "INFO: Creating folder structure...";

echo "INFO: Installing packaging tools..." ;
echo "build" > "requirements.txt" ;
echo "twine" >> "requirements.txt" ;
python -m pip install --upgrade -r requirements.txt ;

touch "LICENSE" ;
touch "README.md" ;
cp "$origin""pyproject_template.toml" "./pyproject.toml" ;
fill_pyproject "$folder_name_" "$python_version_" "$author_name_" "$author_email_" ;
echo "DONE: Created project files.";

mkdir "tests" "src" ;
touch "tests/__init__.py" ;
touch "tests/example_module.py" ;
mkdir "src/$folder_name_" ;
touch "src/$folder_name_/__init__.py" ;
touch "src/$folder_name_/example_module.py" ;
echo "DONE: Created package structure.";

echo "INFO: Verifying Python version in package environment... "$(python --version);

closing_message "$folder_name_" ;

exit 0 ;
