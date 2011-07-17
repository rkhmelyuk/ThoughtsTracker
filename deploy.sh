#!/bin/sh

rm *.pyc
rm thought/*.pyc
rm thought/templatetags/*.pyc

cd ../
tar czvf thoughts.tgz thoughts

scp -i ~/.ssh/mailsight.pem thoughts.tgz ubuntu@staging.mailsight.com:
ssh -i ~/.ssh/mailsight.pem ubuntu@staging.mailsight.com ./deploy-mailsight.sh