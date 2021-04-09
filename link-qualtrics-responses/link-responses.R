# Gather Qualtrics data to a single row per participant.

# For use in studies where a participant begins a Qualtrics survey, leaves the
# survey to complete a task on another site, and then later returns to finish
# the survey. A unique ID must track each participant across each survey view.

# Last updated Thursday, April 8, 2021
# Written in March of 2021 by Michael Pascale


# OPTIONS
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Set the working directory.
working_dir <- "/home/mpascale/doc/wilford/cleaner"

# Name of the file containing the data in CSV format.
data_file <- "/home/mpascale/download/Probation Study_OFFICIAL_April 7, 2021_21.04.csv"

# Name of the output CSV file.
out_file <- "/home/mpascale/doc/wilford/cleaner/Probation Merged.csv"

# Name of the column containing the participant's unique ID or linking variable.
id_field  <- "LinkID"


# SCRIPT
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Set the working directory.
setwd(working_dir)

# Read in the long format data.
df <- read.csv(data_file, na.strings=NA)

# Define a function with which to aggregate the data.
default <- function(subset) {
  
  # Looking only at data in the subset that is not NA or "", return the uniques.
  uniques <- unique(subset[(!is.na(subset)) & (subset != "")])
  
  # If there's more than one unique item, convert the list to a string.
  if (length(uniques) > 1) {
    paste(unlist(uniques), collapse=', ')
    
    # If there's only one unique item, return it.
  } else if (length(uniques) == 1) {
    uniques
    
    # If there are no items, return NA.
  } else {
    NA
  }
}

# Aggregate by id_field to consolidate the data.
wide <- aggregate(df, list(df[,id_field]), default)

# Do some further cleanup.
# For instance, we can reduce the timestamp columns (which right now are comma
# separated) to the earliest or latest timestamp.
for (i in 1:dim(wide)[1]) {
  dates <- unlist(strsplit(wide$StartDate[i], ","))
  dates <- as.POSIXct(dates, format="%m/%d/%Y %H:%M", tz="UTC")
  wide$StartDate[i] <- min(dates)
  
  dates <- unlist(strsplit(wide$EndDate[i], ","))
  dates <- as.POSIXct(dates, format="%m/%d/%Y %H:%M", tz="UTC")
  wide$EndDate[i] <- max(dates)
}

# Write the consolidated data out to a file.
write.csv(wide, out_file)


