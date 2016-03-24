---
layout: project
title: "Mator Smash"
short_name: smash
languages: ['delphi']
status: Standby
repository: matortheeternal/smash
links: ['http://www.nexusmods.com/skyrim/mods/49373/']
date: 2015-01-19 12:00:00 -0800
updated: 2016-03-10 12:00:00 -0800
categories: ['projects']
tags: ['bethesda games', 'applications', 'standalone', 'xEdit', 'conflict resolution']
---
Mator Smash is a full application built on top of the xEdit framework to 
perform automatic conflict resolution.  Most records in Bethesda Plugin (.esp) 
files follow the [rule of one](http://forums.bethsoft.com/topic/775917-compatibility-and-you/), 
by which the game uses the last loaded override of a record.  This means that 
mods which modify the same records need to be patched to work together.

I'll provide a simple example to illustrate this.  Imagine one mod changing the 
name of a weapon, and another mod changing the damage of the weapon.  Only the 
change from the last loaded mod will appear in the game.  That means that 
either the name change or the damage change will appear ingame, depending on 
the order of the plugin files in your load order.

## How it started

The Elder Scrolls IV: Oblivion modders resolved with issue with an application 
called "Wrye Bash".  [Wrye Bash](http://www.nexusmods.com/skyrim/mods/1840/?) 
is a multi-purpose tool, that could (among other things) generate a 
conflict-resolution patch based on tags put into the descriptions of plugin 
files.  Unfortunately, the development work to update Wrye Bash to work with 
Skyrim has progressed extremely slowly, and it still doesn't support handling 
even a fraction of the conflicts for Skyrim that it can handle for Oblivion 
(and it's been over 4 years since Skyrim's release).

I knew from talking with the developers working on updating Wrye Bash for 
Skyrim that they were spending a lot of time porting record definitions to 
interface with Skyrim plugin files from TES5Edit, which had complete and 
verified definitions.  This involve translating Delphi code in Python code 
(because Wrye Bash is built in Python), and was a very time-consuming process. 
I also knew that Wrye Bash's code operated by having hardcoded conflict 
resolution for specific tags.  That is to say, they wrote the conflict 
resolution logic entirely by hand for each and every tag they supported, and 
if they wanted to support a new tag they'd have to write entirely new code. 
This seemed really repetitive to me, and that's where Mator Smash comes in. 
Smash started as an experimental xEdit Script to test an idea I had for generic 
automatic conflict resolution using a recursie traversal algorithm.

## Transitioning to a standalone application

After a month or two of development I had a script which was able to perform 
generic conflict resolution.  It was a little "dumb" because it would always 
forward changes unless a record/subrecord was excluded globally (which isn't 
always the right choice), but it worked.  This was great, but I was finding 
myself unable to iterate quickly because xEdit scripts execute really slowly 
(about 100x slower than native Delphi code).  This made testing and generating 
patches take a really long time (up to an hour, for a large number of 
conflicting plugin files).  The switch to native code was an obvious next step, 
but wouldn't start in earnest until several months later.

Once I had nearly completed my work on Merge Plugins Standalone I started 
working on Mator Smash as a standalone application.  Early on I developed the 
concept of Smash Settings, which are JSON files which indicate what 
records/subrecords to process, and how to process them.  The transition was 
overall really smooth because my experience working on Merge Plugins Standalone 
allowed me to reuse a lot of code.

## Smash Settings

One of the key advancements in Smash which has made it what it is today is the
creation of Smash Settings.  Smash Settings are JSON files within which there 
is a tree which defines the logic for processing records and their subrecords. 
This format allows me to add additional logic by creating additional parameters
to attach to elements in the JSON tree, and allows me to store additional 
metadata with the smash setting such as a name, hash, description, and a color.

However, the biggest advantage Smash Settings offer is a clean, friendly, and 
performant method for users to tap into the smash algorithm and leverage it to
do exactly what they want.  Smash Settings are the reason why I can confidently
say that Smash can perform a superset of conflict resolution compared to previous 
applications such as Wrye Bash.  Smash Settings let users effectively reprogram 
the application, and I've demonstrated how they can be used to imitate the 
functionality of Wrye Bash.

To top it off, because the tree mirrors the structure of records, it's easy to 
construct it and easy to traverse it to extract user settings during the execution 
of the main algorithm.  Ultimately, the JSON format of Smash Settings is the core 
component that makes the User Experience of Smash tick.

## The algorithm

The [algorithm used by Mator Smash](https://github.com/matortheeternal/smash/blob/master/frontend/msAlgorithm.pas) 
is some of the best code I have written to date.  It's rich, powerful, generic, 
and relatively easy to follow.  I'll make an in-depth write-up about this algorithm sometime soon.

## Development status

Mator Smash is currently on standby, which means I'm still working on it but not
as actively as I'd like.  This is because my focus has shifted to Mod Picker, and 
what remains of my dev time is getting sucked up by other projects.  The good news 
is that I am actively working on MADI, which will serve as the backend for Smash. 
So in a way I'm still working on Smash, just indirectly.  ;)