# Prompt definitions for Elicit

study_des = {
"What is the cohort studied in the paper? (e.g., healthy young adults, Parkinson's patients)"
"How many subjects were included in the study?"
"What gait task was performed during EEG recording? (e.g., overground walking, treadmill, obstacle navigation)"
"Was there a secondary task involved during the gait? If yes, describe it."
"What EEG system/manufacturer was used? (e.g., BioSemi, Brain Products)"
"How many EEG channels were recorded?"
"What type of EEG electrodes/channels were used? (e.g., active/passive, wet/dry)"
"Was a dual-layer EEG cap used in the study?"
"What was the EEG sampling frequency in Hz?"
"What software was used for EEG analysis? (e.g., EEGLAB, BrainVision Analyzer)"
}
pre_ICA = {
    "What preprocessing steps were applied before ICA? Please extract steps such as,"
    "Channel rejection method or criteria"
    "Segment/artifact correction methods"
    "Downsampling frequency"
    "Band-pass, high-pass, low-pass, or band-stop filter settings"
    "Line noise removal method (e.g., CleanLine, notch filter)"
    "Re-referencing strategy"
    "Artifact Subspace Reconstruction (ASR) usage"
    "iCanClean usage"
    "Epoching method (if any)"
}

ICA = {
    "What ICA algorithm was used (e.g., Infomax, FastICA)?"
    "How many ICA components were computed?"
    "How were components selected for rejection? (e.g., ICLabel, manual, MARA)"
    "What criteria were used for rejecting components?"
    "Was IC clustering performed? If so, what method?"
}

post_ICA = {
    "What preprocessing steps were applied after ICA? Include if any:"
    "Channel/segment rejection"
    "Filter settings (high-pass, low-pass, band-pass)"
    "Re-referencing"
    "Channel interpolation"
    "Downsampling"
    "Epoching strategy"
    "Source localization techniques"
    "Any analysis of 1/f component or baseline correction"
}

flow_preprocessing_steps = {"List the full sequence of EEG preprocessing steps described in the paper in the order they were applied. Include all relevant filters, re-referencing, artifact rejection, ICA, and post-ICA processing. List them as a step-by-step procedure. If not reported or unclear, write 'Not reported'"}