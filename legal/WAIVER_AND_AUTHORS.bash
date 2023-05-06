GIT_USERNAME=$(git config user.name)
GIT_EMAIL=$(git config user.email)
echo $GIT_USERNAME "<"$GIT_EMAIL">" >> AUTHORS
gpg --no-version --armor --sign WAIVER;
cat WAIVER.asc >> AUTHORS; 
# echo -e '\n' >> AUTHORS; 
cat WAIVER.asc; 
rm -rf WAIVER.asc