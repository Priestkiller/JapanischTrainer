plugins { id("com.android.application"); id("org.jetbrains.kotlin.android") }
android {
    namespace = "de.priestkiller.japanischtrainer"
    compileSdk = 35
    defaultConfig {
        applicationId = "de.priestkiller.japanischtrainer"
        minSdk = 28
        targetSdk = 35
        versionCode = 11000401
        versionName = "11.0.4-android.1"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        testInstrumentationRunnerArguments["additionalTestOutputDir"] = "/sdcard/Android/media/de.priestkiller.japanischtrainer.test/test-evidence"
        ndk { abiFilters += listOf("arm64-v8a", "x86_64") }
    }
    buildTypes {
        release { isMinifyEnabled = false }
        debug { applicationIdSuffix = ".test"; versionNameSuffix = "-test" }
    }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
    kotlinOptions { jvmTarget = "17" }
    buildFeatures { buildConfig = true }
    sourceSets.getByName("main") {
        assets.srcDirs("../web", "../generated/assets")
    }
    androidResources { noCompress += listOf("onnx", "bin") }
}
dependencies {
    implementation("androidx.webkit:webkit:1.12.1")
    implementation("androidx.core:core-ktx:1.15.0")
    implementation(files("../vendor/sherpa-onnx-1.13.8.aar"))
    androidTestImplementation("androidx.test:runner:1.6.2")
    androidTestImplementation("androidx.test:rules:1.6.1")
    androidTestImplementation("androidx.test.ext:junit:1.2.1")
}
