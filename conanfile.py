#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, shutil
from conans import ConanFile, CMake, tools
from conans.errors import ConanException


class RingbufferConan(ConanFile):
    name = "ringbuffer"
    version = "1.0.2"
    description = "Primitive ringbuffer implementation for bud. Can be used with gypkg."
    url = "https://github.com/alekseevx/conan-ringbuffer"
    license = "MIT"
    exports_sources = "CMakeLists.txt"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    options = {}    

    def source(self):
        shutil.rmtree("src", ignore_errors=True)
                    
        tools.get(
            url="https://github.com/gypkg/ringbuffer/archive/v{ver}.tar.gz".format(ver=self.version),
            sha256="daf9ff2e7cc94b95094f69ea616e5194b9f517fde12f845044e4f75430e3bfec"
        )
        source_dir = "{name}-{version}".format(name=self.name, version=self.version)
        shutil.move(source_dir, "src")
        shutil.copy(src="CMakeLists.txt", dst="src")

    def configure(self):
        del self.settings.compiler.libcxx
        if self.settings.compiler == "Visual Studio" and int(str(self.settings.compiler.version)) < 14:
            raise ConanException("Visual Studio >= 14 (2015) is required")

    def requirements(self):
        self.requires("cmake_installer/3.10.0@conan/stable", private=True)

    def build(self):
        shutil.rmtree("build", ignore_errors=True)
        os.mkdir("build")

        cmake = CMake(self)
        cmake.verbose = True        
        cmake.configure(source_dir="../src", build_dir="build")
        cmake.build()

    def package(self):
        self.copy("src/README.md", dst=".", keep_path=False)
        self.copy("*.h", src="src", dst="include", keep_path=False)
        self.copy("*.a", src="build/lib", dst="lib", keep_path=False)
        self.copy("*.lib", src="build/lib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

