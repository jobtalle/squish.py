# Squish.py

A web app compressor utility.

This works by inlining source files referenced by an HTML page. It currently inlines and compresses the following sources:

* CSS
* Javascript
* GLSL shaders (found as strings inside javascript)

This is a tool I use personally; it works for my coding style, but it may be incompatible with others.

## Usage

`python squish.py <source> <target>`

Source is the source HTML file containing references to included CSS and JS, target should be another HTML file where everything is inlined.

## Flags

| Flag | Usage |
| --- | --- |
| --advanced-cc | Use [advanced closure compiler optimizations](https://developers.google.com/closure/compiler/docs/compilation_levels) |
