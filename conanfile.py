from conans import ConanFile, CMake, tools
import os


class LibrdkafkaConan(ConanFile):
    name = "librdkafka"
    version = "1.2.2"
    description = "The Apache Kafka C/C++ library"
    topics = ("conan", "librdkaka", "kafka")
    url = "http://bitbucket-idb.nyoffice.tradeweb.com:7990/scm/tp/conan-librdkafka.git"
    homepage = "https://github.com/edenhill/librdkafka"
    license = "BSD-2-Clause"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    requires = (
        'OpenSSL/1.1.1d@conan/stable',
        'zlib/1.2.11@conan/stable'
    )

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["RDKAFKA_BUILD_STATIC"] = not self.options.shared
        cmake.definitions["RDKAFKA_BUILD_EXAMPLES"] = False
        cmake.definitions["RDKAFKA_BUILD_TESTS"] = False
        cmake.definitions["ENABLE_LZ4_EXT"] = False
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can just remove the lines below
        include_folder = os.path.join(self._source_subfolder, "include")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['rdkafka++', 'rdkafka']
        if not self.options.shared:
            self.cpp_info.defines.append('LIBRDKAFKA_STATICLIB')
        if self.settings.os == 'Linux':
            self.cpp_info.libs.extend(['rt', 'dl', 'pthread'])
