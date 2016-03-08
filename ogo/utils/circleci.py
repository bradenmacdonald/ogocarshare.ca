"""
Utility code to create private.yml from vars in circle.yml
"""

import yaml

if __name__ == '__main__':
    with open('private.yml', 'x') as outfile, open('circle.yml') as infile:
        private_config = yaml.load(infile.read())["private_config"]
        outfile.write(yaml.dump(private_config))
