# Creating a custom MSE Hub

Follow these instructions to set up your own MSE Hub.

## Prerequisites

### Install Github Desktop

This isn't strictly necessary, but promise me, it'll make your life a lot easier. You can get GH Desktop [here](https://desktop.github.com/download/).

### Install Python

This one *is* strictly necessary, as the script that builds the entire site is written in Python. You can get it [here](https://www.python.org/downloads/).

## Step 1: Fork me

If you're reading this, you're probably already here, but in case you aren't, navigate to https://github.com/magictheegg/mse-hub/. At the top, click the "Fork" button to start creating your own fork of the code.

![Fork](https://github.com/magictheegg/mse-hub-readme/blob/main/fork.png?raw=true)

On the next page, **change the "Repository name" field** to \<your-github-username\>.github.io. This is **critical** for making your code actually deploy to Github sites. You can add a Description if you want. Keep "Copy the `main` branch only" checked. Once you've renamed the repository, click "Create fork".

![Fork part 2](https://github.com/magictheegg/mse-hub-readme/blob/main/fork-part-two.png?raw=true)

Once the fork is created, you'll see the code in Github. Now it's time to move to Github desktop.

Once you've logged into Github Desktop, click File => Clone repository ... and you should see your forked repository in the repo list. Click it, then choose clone. When the "How are you planning to use this fork?" modal pops up, select "For my own purposes," then Continue.

![How are you planning to use this fork?](https://github.com/magictheegg/mse-hub-readme/blob/main/how-fork.png?raw=true)

Finally, in the bar along the top, select "Fetch origin" to pull the origin into your forked repo.

## Step 2: Exporting set files

> :memo: **Note:** This exporter uses the "Title" and "Set code" entered in the "Set info" tab of your MSE set. If those aren't set, the exporter will exhibit strange behavior.

In the resources folder of your cloned repo, you'll find the "magic-egg-allinone" exporter. Copy that into the "data" folder of MSE, then open the program. Open a set you'd like to export, then click File => Export => HTML ... and select Egg's All-in-One. This exporter currently exports two files:
 - \<code>-files directory containing all the files necessary to export the set
 - Draftmancer file used to draft your set

You can reference the [Draftmancer export guide](https://docs.google.com/document/d/1xPqa91WrBqJ7t7pFJvXFUgKUDgtPe-Yeem35IOq2Qcc/edit) for more detailed instructions on that half of the exporter, but I'll quickly go over each option:
- **Export images**: Defaults to "yes". You should do this every time or you might get weird results with some of your site image pages.
- **Export draft file**: Defaults to "yes". Only unselect this if your set is never meant to be drafted.
- **Github repo**: The name of the repo you just forked, which should be in the format of \<gh-username>.github.io.
- **Rares / Uncommons / Commons / Wildcards**: Number of cards at each rarity that show up in a draft booster of your set.
- **Land slot**: Defaults to "no". If you are denoting cards in your set with the "!landslot" note, flip this to "yes" to assign those cards their own draft slot.

Once each of these options is filled out, click OK and save the set file as "\<set_code>.txt". (This should match the "Set code" in your "Set info" tab.) This will take a second as the application exports all your images, and the end result is two outputs:
- **\<code>.txt**, which is irrelevant.
- **\<code>-files**, a directory containing all the files necessary to publish your set onto your hub.

## Future Updates

To get updates to the scripts or resources, from Github Desktop, select "Current branch" in the bar along the top, the at the bottom of the opened menu click "Choose a branch to merge into **main**". On the next modal, select "upstream/main", then click "Create a merge commit". This will bring all new code in the main repo into your forked repo, and it will be ready to push the next time you push the contents of your site to main.
