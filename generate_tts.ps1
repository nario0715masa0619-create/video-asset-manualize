# generate_tts.ps1
param (
    [string]$text,
    [string]$output_file
)

Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SetOutputToWaveFile($output_file)
$synth.Speak($text)
$synth.Dispose()
