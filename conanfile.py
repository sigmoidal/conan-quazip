import os
import shutil
from conans import ConanFile, CMake, tools

# conan create . bincrafters/testing --build missing -o quazip:shared=True
# conan create . bincrafters/testing --build missing -o quazip:shared=False

class QuazipConan(ConanFile):
    name = "quazip"
    version = "0.8.1"
    license = "LGPL-2.1, zlib/png"
    url = "https://github.com/sigmoid/conan-quazip"
    homepage = "https://github.com/stachenov/quazip"
    description = "QuaZIP is the C++ wrapper for Gilles Vollant's ZIP/UNZIP package (AKA Minizip) using Trolltech's Qt library."
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    requires = "zlib/1.2.11@conan/stable", "qt/5.13.2@bincrafters/stable"

    options = { "shared": [True, False],
                "fPIC": [True, False] }

    default_options = { 'shared': True,
                        'fPIC': False,
                        'qt:shared': True,
                        'zlib:shared': False,
                        "qt:with_sqlite3": True,
                        "qt:with_odbc": False,  
                        "qt:with_pq": False,  
                        "qt:with_mysql": False,
                        "qt:with_sdl2": False,  
                        "qt:with_openal": False }

    exports_sources = ["CMakeLists.txt", "CMakeLists-upstream.txt"]

    _source_subfolder = "source_subfolder"


    def configure(self):
        if self.settings.compiler == 'Visual Studio':
            del self.options.fPIC

    def source(self):
        sha256 = "4fda4d4248e08015b5090d0369ef9e68bdc4475aa12494f7c0f6d79e43270d14"
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = "%s-%s" % (self.name, self.version)
        os.rename(extracted_dir + '/quazip', self._source_subfolder)

        # copy the license file into the new sourcedir (so we can copy it later into the package)
        shutil.copy(extracted_dir + '/COPYING', self._source_subfolder)
        shutil.copy('CMakeLists-upstream.txt', self._source_subfolder + '/' + 'CMakeLists.txt')

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["QUAZIP_BUILD"] = True

        if not self.options.shared:
            cmake.definitions["QUAZIP_STATIC"] = True

        cmake.definitions["BUILD_STATIC_LIBS"] = not self.options.shared
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared

        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()


    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)


    def package_info(self):
        if not self.options.shared:
            self.cpp_info.defines.append('QUAZIP_STATIC')

        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.bindirs = ['bin']
        self.cpp_info.libdirs = ['lib']
