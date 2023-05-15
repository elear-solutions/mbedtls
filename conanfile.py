from conans import ConanFile, CMake

class ElearcommonlibConan(ConanFile):
    name = "mbedtls"
    version = "0.0.1"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "This recipe file used to build and package binaries of elearcommon repository"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [ True, False ],
        "color": [ True, False ],
        "cmake_build_type": [ "Debug", "Release" ]
    }
    default_options = { "shared": False , "color": False, "cmake_build_type": "Release" }
    generators = "cmake"
    default_user = "jenkins"
    default_channel = "master"

    def requirements(self):
        if self.user and self.channel:
            default_user = self.user
            default_channel = self.channel

    def build(self):
        cmake = CMake(self)
        cmake.definitions["Platform"] = self.settings.os
        cmake.definitions["COLOR"] = self.options.color
        cmake.definitions["CMAKE_BUILD_TYPE"] = self.options.cmake_build_type
        cmake.configure(source_folder=".")
        cmake.build()
        cmake.install()

    def package(self):
        #here src is directory path from where it should start checking for .h files and all mentioned in self.copy()
        #it checks recursively by default
        self.copy("*.h", dst="include/mbedtls", src="package/include/mbedtls")
        self.copy("*", dst="lib", src="package/lib", keep_path=False)

    def package_info(self):
        #self.cpp_info.libs name will be used to attach library in CMakelists.txt
        self.cpp_info.libs = [ "mbedtls", "mbedtls_static"]
