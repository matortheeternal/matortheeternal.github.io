---
layout: project
title: "Forge Menu Overhaul"
short_name: FMO
languages: ['delphi']
status: Inactive
repository: matortheeternal/TES5EditScripts
links: ['http://www.nexusmods.com/skyrim/mods/37003/']
date: 2013-06-08 13:05:00 -0800
updated: 2015-04-04 12:00:00 -0800
categories: ['projects']
tags: ['bethesda games', 'automation', 'scripting', 'skyrim']
---
Forge Menu Overhaul was my first programming project (my first time 
programming, more accurately) and my introduction to the Skyrim modding scene. 
FMO was conceived to combat the issue of cluttered blacksmith forge menus in 
Skyrim when you had added a lot of Armor mods to the game.  

The Skyrim forge menu was developed with console gaming in mind, and became 
really cumbersome to use when there were a lot of options to craft for a given 
material.  The most logical way to resolve this issue would be to change the 
entire menu, or to add new material categories for new armors.  The issue was 
that the menu was coded in actionscript, located somewhere deep in the game's 
code, and not really exposed to modders.  The [SkyUI](http://www.nexusmods.com/skyrim/mods/3863/) 
team was able to modify this, so I reached out to them to see if they would be 
tackling the forge menu sometime soon.  Their answer: nope.

This led me to try to come up with my own solution.  I couldn't add categories,
but I could modify the conditions under which recipes would appear in the menu. 
Some mods had already tried tackling this by adding items to the game which,
when carried, would show certain recipes in the forge menu.  But this still
required managing the items you're carrying, and wasn't a really flexible
solution.

## The hack
I came up with an approach where I'd add new items to the game that would make
recipes for a given armor/weapon set appear in the forge menu, but also add new
recipes to craft these items directly from the forge.  This would allow me to 
make a sub-category for, say, "Red Glass" armor and weapons, and then open that
sub-category while at the forge by simply crafting it!  The only issue then was 
how to close the category, and I figured that could be done by adding a second 
recipe for each armor/weapon set which would require the item which makes the
set appear to be available, and would consume the item that makes the set 
available as well.  The final touch was making these items weightless, 
valueless, and non-playable (which makes them not appear in the player's 
inventory).  This made them essentially non-existent items, but still allowed a 
player to track the sub-categories they had opened between forges, or between 
gaming sessions.

For the purposes of my implementation I called these items "AActivators" and 
"DActivators".  And they worked.

## Automating it
I realized fairly quickly that applying my approach to every armor and weapon 
in the game would cost me a lot of time.  With over 4000 armor mods on Nexus
Mods, I just didn't see myself spending a year of my life making all of them 
work with this approach.  This led me to seek the advice and counsel of zilav,
one of the developers of [TES5Edit](https://github.com/TES5Edit/TES5Edit) - a 
modding tool I had used to build plugins for my mod.  Zilav had recently added 
the ability to execute scripts through TES5Edit, which would allow me to 
automate the FMO process.

Over several months I conversed with zilav, exchanging code snippets, asking
questions, and learning about coding and best practices.  By the end of it all 
I had a working script which would generate a patch file for the mods a user 
had loaded in TES5Edit which would apply my "hack" solution, making the forge 
more usable.  It hadn't been particularly easy, but I finally fixed the 
problem.  And, along the way, I had learned to code.

So began my career as a software developer.

## Implementation
One of the coolest aspects of the FMO script which I'm amazed I was able to do
at the beginning of my coding career (albeit terribly) was recognizing armors
and weapons that were part of a set.  I did this by doing string analysis of 
their ingame display names, constructing a set of prefixes corresponding to the 
armors and weapons the script found.  This is not a simple process, as prefixes 
can be multiple words long, some mod authors use irregular suffixes, and 
suffixes and can be more than one word long.  Performing this process requires 
a non-trivial algorithm.  Looking back I know I could do it in a fraction of 
the lines of code now, but I respect that I was able to do it at all back when 
I was working on FMO before having any sort of computer science education or 
any experiences to draw on.

## Development status
As of right now FMO hasn't been updated for several years.  More interesting
projects have been taking up my time.  I do want to update it sometime, though
I'm not really sure when.  Ultimately, it may never get updated, and I'm ok 
with that.  It was a really cool script, but it wasn't particularly popular
(it has just over 200 endorsements on Nexus Mods to date).