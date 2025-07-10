##############################
# Designed to only run once  #
# Install necessary packages #
# Saves pre-processed data   #
##############################


# Pick file path
wd <- "C:/Users/BJW95/OneDrive - University of Pittsburgh/Documents/Projects/Delegation"
# wd <- "C:/Users/bjwil/OneDrive - University of Pittsburgh/Documents/Projects/Delegation"
setwd(wd)

### Install gmoTree ###

# Dependencies
install.packages(c(
  # "data.table", 
  "knitr", 
  "openxlsx", 
  "pander", 
  "plyr", 
  "rlist", 
  "rmarkdown"
))

# From a .tar.gz or .zip file:
install.packages(paste(wd, "/Packages/gmoTree_1.4.1.tar.gz", sep=""), repos = NULL, type = "source")

### Install other packages ### 

# List of CRAN packages
cran_packages <- c(
  "foreign", 
  "plm", 
  "stargazer", 
  "patchwork", 
  "ks", 
  "lmtest",
  "dplyr", 
  "stringr", 
  "tidyr", 
  "ggplot2", 
  "svglite", 
  "AER",
  "estimatr"
)

# Install missing CRAN packages
installed <- rownames(installed.packages())
for (pkg in cran_packages) {
  if (!pkg %in% installed) {
    install.packages(pkg)
  }
}

# List of CRAN packages
cran_packages <- c(
  "foreign", 
  "plm", 
  "stargazer", 
  "patchwork", 
  "ks", 
  "lmtest",
  "dplyr", 
  "stringr", 
  "tidyr", 
  "ggplot2", 
  "svglite", 
  "AER",
  "estimatr"
)

# Load all packages
lapply(c("gmoTree", cran_packages), library, character.only = TRUE)


### Clean data using gmoTree ###

# Load in data
path <- paste(wd, "/Data", sep="")

rawData <- import_otree(path=path)
rawData<- delete_duplicate(rawData)
rawData <- make_ids(rawData)
rawData <- messy_time(rawData,combine = TRUE,info = TRUE)
rawData <- messy_chat(rawData,combine = TRUE,info = TRUE)
rawData <- delete_dropouts( rawData,final_apps = "payment", info = FALSE )
rawData <- assignv(rawData,  variable = "session.config.take_it_or_leave_it", newvar="offer.treat")
rawData <- assignv(rawData,  variable = "session.config.chat", newvar="chat.treat")

# Chats

match_chats_to_rounds <- function(Chats, Rounds) { 
  # Get chat end times by session and channel
  chat_endings <- Chats %>%
    group_by(session_code, channel) %>%
    summarise(
      chat_end_time = max(timestamp),
      participant_codes = list(unique(participant_code)),
      .groups = "drop"
    ) %>%
    tidyr::unnest(participant_codes, names_repair = "minimal") %>%
    rename(participant_code = participant_codes)
  
  # Join with rounds to find valid round completions after the chat
  matched <- chat_endings %>%
    left_join(Rounds, by = c("session_code", "participant_code"), relationship="many-to-many") %>%
    filter(chat_end_time <= epoch_time_completed+2) %>% #Allowing for rounding error
    group_by(session_code, channel, participant_code) %>%
    slice_min(epoch_time_completed, with_ties = FALSE) %>% # Closest round after chat
    ungroup()
  
  return(matched)
}

Chats <- rawData$Chats
Rounds <- subset(rawData$Time, app_name=="veto_delegation" & page_name=="Chat")
matched_chats <- as.data.frame(match_chats_to_rounds(Chats, Rounds))

chat_summary <- Chats %>%
  arrange(session_code, channel, timestamp,participant_code) %>%
  mutate(line = str_c(nickname, ": ", body)) %>%
  group_by(session_code, channel) %>%
  summarise(chat_text = str_c(line, collapse = "\n"), .groups = "drop") %>%
  as.data.frame()

round_mapping <- as.data.frame(unique(matched_chats[ ,c('session_code','channel', 'round_number' )]))

chat.df <- inner_join(chat_summary,round_mapping,by=c("session_code","channel"))

chat.p.df <- left_join(matched_chats[, c('session_code','channel','participant_code')], chat.df , by=c('session_code','channel') )

# Main treatment data 

delegData <- rawData$veto_delegation
delegData$t <- delegData$subsession.round_number
delegData$session_code <- delegData$session.code
delegData$participant_code <- delegData$participant.code
delegData$round_number <- delegData$subsession.round_number
delegData$i <- delegData$participant_id
delegData$role <- delegData$player.role
delegData$minX <- delegData$group.minSlider
delegData$maxX <- delegData$group.maxSlider
delegData$y <- delegData$group.response
delegData$pay <- delegData$player.payoff
delegData$theta <- delegData$group.vetoer_bias
delegData$urn <- delegData$group.roundName
delegData$delegation <- ifelse(delegData$offer.treat, FALSE,TRUE)
delegData$chat <- ifelse(delegData$chat.treat, TRUE,FALSE)
delegData <- left_join(delegData, chat.p.df , by=c('session_code','participant_code','round_number') )
data <- delegData[, c('i','t','role','minX','maxX','y', 'pay','theta','urn',"delegation","chat",'chat_text')]

# Save

saveRDS(data, file = "Data/deleg_data.rds")

# Save chat logs separately

chats.joined.df <- unique(subset(data, chat==TRUE )[ , c('delegation','t','urn','theta', 'chat_text','minX','maxX','y')])
chats.joined.df$mech <- ifelse(chats.joined.df$delegation, "Delegation",'TIOLI')
head(chats.joined.df)

export_chat_transcripts <- function(df, filepath) {
  # Open a connection
  con <- file(filepath, open = "wt")
  on.exit(close(con))
  df_sorted <- df %>% arrange(delegation, t)
  
  for (i in seq_len(nrow(df_sorted))) {
    row <- df_sorted[i, ]
    
    # Format the entry
    entry <- paste0(
      strrep("_", 50), "\n",
      sprintf("Round %d (%s), Urn=%s, theta=%d.", row$t, row$mech, row$urn, row$theta), "\n",
      strrep("-", 50), "\nChat log:\n",
      row$chat_text, "\n", strrep("-", 50), "\n",
      sprintf("\tSeller offer: %d-%d.\tBuyer choice: %d", row$minX, row$maxX, row$y), "\n",
      strrep("_", 50), "\n\n"
    )
    
    # Write to file
    writeLines(entry, con)
  }
  
  message("Export complete: ", filepath)
}
export_chat_transcripts(chats.joined.df, "Data/chat_transcripts.txt")

# Robot choices data

robotData <- rawData$robot
robotData$t <- robotData$subsession.round_number
robotData$session_code <- robotData$session.code
robotData$participant_code <- robotData$participant.code
robotData$round_number <- robotData$subsession.round_number
robotData$i <- robotData$participant_id
robotData$minX <- robotData$player.minSlider
robotData$maxX <- robotData$player.maxSlider
robotData$delegation <- ifelse(robotData$offer.treat, FALSE,TRUE)
robotData$chat <- ifelse(robotData$chat.treat, TRUE,FALSE)
robotData$urn <- robotData$player.roundName
robot <- robotData[, c('i','t','minX', 'maxX', 'urn', "delegation","chat")]

# Save
saveRDS(robot, file = "Data/deleg_robot.rds")

# Lottery Choices data

lotteryData <- rawData$lotteries
lotteryData$t <- lotteryData$subsession.round_number
lotteryData$session_code <- lotteryData$session.code
lotteryData$participant_code <- lotteryData$participant.code
lotteryData$round_number <- lotteryData$subsession.round_number
lotteryData$i <- lotteryData$participant_id
lotteryData$lottery <- lotteryData$player.lottery
lotteryData$delegation <- ifelse(lotteryData$offer.treat, FALSE,TRUE)
lotteryData$chat <- ifelse(lotteryData$chat.treat, TRUE,FALSE)
lottery <- lotteryData[, c('i','t','lottery',"delegation","chat")]
lottery_types <- c("DelLow", "TIOLILow", "DelMid", "TIOLIMid", "DelHigh", "TIOLIHigh")
lottery$lotteryType <- lottery_types[lottery$t]

all_lotteries <- list(
  DelLow = list(
    "Lottery A" = list(action = "{0} U [1,8]"),
    "Lottery B" = list(action = "{0} U [3,8]"),
    "Lottery C" = list(action = "{0} U [5,8]"),
    "Lottery D" = list(action = "{0} U [7,8]")
  ),
  TIOLILow = list(
    "Lottery A" = list(action = "{0,1}"),
    "Lottery B" = list(action = "{0,3}"),
    "Lottery C" = list(action = "{0,5}"),
    "Lottery D" = list(action = "{0,7}")
  ),
  DelMid = list(
    "Lottery A" = list(action = "{0} U [1,8]"),
    "Lottery B" = list(action = "{0} U [3,8]"),
    "Lottery C" = list(action = "{0} U [5,8]"),
    "Lottery D" = list(action = "{0} U [7,8]")
  ),
  TIOLIMid = list(
    "Lottery A" = list(action = "{0,1}"),
    "Lottery B" = list(action = "{0,3}"),
    "Lottery C" = list(action = "{0,5}"),
    "Lottery D" = list(action = "{0,7}")
  ),
  DelHigh = list(
    "Lottery A" = list(action = "{0} U [1,8]"),
    "Lottery B" = list(action = "{0} U [3,8]"),
    "Lottery C" = list(action = "{0} U [5,8]"),
    "Lottery D" = list(action = "{0} U [7,8]")
  ),
  TIOLIHigh = list(
    "Lottery A" = list(action = "{0,1}"),
    "Lottery B" = list(action = "{0,3}"),
    "Lottery C" = list(action = "{0,5}"),
    "Lottery D" = list(action = "{0,7}")
  )
)

get_min_max_x <- function(lottery_type, lottery_name) {
  action <- all_lotteries[[lottery_type]][[lottery_name]]$action
  
  if (startsWith(lottery_type, "Del")) {
    match <- stringr::str_match(action, "\\[(\\d+),(\\d+)\\]")
    minX <- as.numeric(match[2])
    maxX <- as.numeric(match[3])
  } else if (startsWith(lottery_type, "TIOLI")) {
    match <- stringr::str_match(action, "\\{\\d+,(\\d+)\\}")
    val <- as.numeric(match[2])
    minX <- val
    maxX <- val
  } else {
    minX <- NA
    maxX <- NA
  }
  
  return(c(minX, maxX))
}

lottery <- lottery %>%
  rowwise() %>%
  mutate(
    result = list(get_min_max_x(lotteryType, lottery)),
    lotteryMinX = result[1],
    lotteryMaxX = result[2]
  ) %>%
  select(-result) %>%
  ungroup()

lottery <- lottery %>%
  mutate(
    neutralMinX = case_when(
      lotteryType == "DelLow"     ~ 1,
      lotteryType == "TIOLILow"   ~ 5,
      lotteryType == "DelMid"     ~ 5,
      lotteryType == "TIOLIMid"   ~ 5,
      lotteryType == "DelHigh"    ~ 7,
      lotteryType == "TIOLIHigh"  ~ 7,
    )
  )

# Add urn_type column based on the lotteryType
lottery <- lottery %>%
  mutate(
    urn = case_when(
      grepl("Low", lotteryType) ~ "Low",
      grepl("Mid", lotteryType) ~ "Middle",
      grepl("High", lotteryType) ~ "High",
      TRUE ~ NA_character_
    ),
    type = case_when(
      grepl("Del", lotteryType) ~ "Delegation",
      grepl("TIOLI", lotteryType) ~ "TIOLI",
      TRUE ~ NA_character_
    )
  )

# Save
saveRDS(lottery, file = "Data/deleg_lottery.rds")

# Other regarding choices data

dictatorData <- rawData$dictator
dictatorData$t <- dictatorData$subsession.round_number
dictatorData$round_number <- dictatorData$subsession.round_number
dictatorData$i <- dictatorData$participant_id
dictatorData$type <- dictatorData$player.dictator_type
dictatorData$X <- dictatorData$player.dictator_choice
dictatorData$delegation <- ifelse(dictatorData$offer.treat, FALSE,TRUE)
dictatorData$chat <- ifelse(dictatorData$chat.treat, TRUE,FALSE)
dictator <- dictatorData[, c('i','t','type', 'X', "delegation","chat")]

dictator <- dictator %>% 
  mutate(
    urn = case_when(
      type == 1 ~ 'Low',
      type == 3 ~ "Middle",
      type == 6 ~ "High"
    ),
    action = case_when(
      # Middle alignment (type == 3)
      type == 3 & X == 1 ~ 3,
      type == 3 & X == 2 ~ 4,
      type == 3 & X == 3 ~ 5,
      type == 3 & X == 4 ~ 6,
      
      # Low alignment (type == 1)
      type == 1 & X == 1 ~ 2,
      type == 1 & X == 2 ~ 3,
      type == 1 & X == 3 ~ 4,
      type == 1 & X == 4 ~ 2,
      
      # High alignment (type == 6)
      type == 6 & X == 1 ~ 5,
      type == 6 & X == 2 ~ 6,
      type == 6 & X == 3 ~ 7,
      type == 6 & X == 4 ~ 8,
      
      TRUE ~ NA_real_
    ),
    maxAction = case_when(
      type == 1 ~ 4,
      type == 3 ~ 6,
      type == 6 ~ 8,
      TRUE ~ NA_real_
    )
  )



# Save
saveRDS(dictator, file = "Data/deleg_dictator.rds")


