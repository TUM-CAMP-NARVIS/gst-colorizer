from conans import ConanFile, CMake, tools
import os

class GstreamerColorizerConan(ConanFile):
    name = "gstreamer-colorizer"
    version = "0.1"
    license = "LGPL"
    description = "Plugin to colorize 16 bit grayscale depth images with a color map"
    url = "https://aivero.com"
    settings = "os", "arch", "compiler", "build_type"
    exports_sources = ["CMakeLists.txt", "src/*"]

    # def set_version(self):
    #     git = tools.Git(folder=self.recipe_folder)
    #     tag, branch = git.get_tag(), git.get_branch()
    #     self.version = tag if tag and branch.startswith("HEAD") else branch

    # def build_requirements(self):
    #     self.build_requires("cmake/[>=3.15.3]@%s/stable" % (self.user))

    def requirements(self):
        gst_version = "master" if self.version == "master" else "[~%s]" % "1.16.2"
        gst_channel = "testing" if self.version == "master" else "stable"

        self.requires("gstreamer-plugins-base/%s@%s/%s" % (gst_version, self.user, gst_channel))

    def build(self):
        env = {
            "GIT_PKG_VER": "%s" % self.version,
        }
        with tools.environment_append(env):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()
            cmake.install()

    def package_info(self):
        self.env_info.GST_PLUGIN_PATH.append(os.path.join(self.package_folder, "lib", "gstreamer-1.0"))
