# cmake-checker
cmake-checker is a tool to search for violations to 'modern' cmake rules.

### Usage

```
usage: __main__.py [-h] [--warn-only] [--reporter {console,junit}]
                        [-o OUTPUT_FILE] [--whitelist WHITELIST]
                        PATH [PATH ...]

positional arguments:
  PATH                  Path to the file or directory where the checks should
                        be done

optional arguments:
  -h, --help            show this help message and exit
  --warn-only           Program will return 0 even if violations are found
  --reporter {console,junit}
                        Specify type of reporter to output
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Output results to file with given name
  --whitelist WHITELIST
                        Whitelist file with rules to ignore certain files or
                        dirs (.gitignore style)
```

### What&Why tool warns about
* `file(GLOB ...)` 

    * CMake will not track the dependencies of a new file on disk correctly. If no CMakeLists.txt file changes when a source 
    is added or removed then the generated build system cannot know when to ask CMake to regenerate.
    * You can't ensure that only files you want are added. Globbing may pick up stray files that you do not want.
* Functions
    * `add_compile_options`
    * `add_compile_definitions`
    * `link_libraries`
    * `add_definitions`
    * `include_directories`
    
    Functions work on directory scope instead of target scope. Every single one of listed functions has 
    equivalent for target scope which should be used.
* Properties `COMPILE_<LANG>_FLAGS`

    These properties should be set for a target - not modified globally
* Closing commands with clauses 
    * `endif`
    * `endfunction`
    * `endmacro`
    * `endforeach`
    
    Example:   
    ```
    macro(foo ...)
    ...
    endmacro(foo)
    ```
* Set/unset including
    * `ENV`
    * `CACHE`
* `../..` in `target_sources` function
* Set/unset `PARENT_SCOPE` outside of function declaration

### Possibility to disable check
If you need to disable for any specific reasons checks you can do it using:
```
# cmake-check disable
...
# cmake-check enable
```
