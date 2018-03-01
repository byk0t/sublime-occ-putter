#Oracle Commerce Cloud Design Code Utility package for Sublime Text 3

1. Download Design Code Utility from Oracle

2. Grab your project from OCC
`dcu --grab --node $node_url --username $username --password $password`

3. Create Sublime Text 3 project from the folder with grabbed source code

4. Install the plugin (clone the project, make archive and place it into Installed Packages)

`rm -rf occPut.sublime-package && zip -r occPut.sublime-package ./* -x *.git* && cp -r occPut.sublime-package ~/.config/sublime-text-3/Installed\ Packages/`

5. Use Project->Occ Put->Initialize settings for setup settings

6. Update will start when you press Ctrl+S combination
