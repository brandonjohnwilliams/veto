# List of CRAN packages
cran_packages <- c(
  "foreign", "plm", "stargazer", "patchwork", "ks", "lmtest",
  "dplyr", "stringr", "tidyr", "ggplot2", "svglite", "AER",
  "estimatr"
)

# Install missing CRAN packages
installed <- rownames(installed.packages())
for (pkg in cran_packages) {
  if (!pkg %in% installed) {
    install.packages(pkg)
  }
}

# Install gmoTree 
# Dependencies
install.packages(c(
  "data.table", "knitr", "openxlsx", "pander", 
  "plyr", "rlist", "rmarkdown"
))

# From a .tar.gz or .zip file:
install.packages("C:/Users/Brandon/Downloads/gmoTree_1.4.1.tar.gz", repos = NULL, type = "source")


# Load all packages
lapply(c("gmoTree", cran_packages), library, character.only = TRUE)

# Load in data
path <- "C:/Users/bjw95/Downloads/data"

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
delegData$theta <- delegData$group.vetoer_bias
delegData$urn <- delegData$group.roundName
delegData$delegation <- ifelse(delegData$offer.treat, FALSE,TRUE)
delegData$chat <- ifelse(delegData$chat.treat, TRUE,FALSE)
delegData <- left_join(delegData, chat.p.df , by=c('session_code','participant_code','round_number') )
data <- delegData[, c('i','t','role','minX','maxX','y','theta','urn',"delegation","chat",'chat_text')]

subject_counts <- data %>%
  distinct(i, delegation, chat) %>%  # Ensure uniqueness by participant and treatment
  group_by(delegation, chat) %>%
  summarise(n_subjects = n(), .groups = 'drop')

as.data.frame(subject_counts)



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
export_chat_transcripts(chats.joined.df, "chat_transcripts.txt")

#### DONE PRE-PROCESSING ####

# Plots of minimum offers

p1 <-ggplot(subset(data,urn=="Low" & t>10 & role=="Seller" & delegation==FALSE & chat==FALSE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth =1,color = "#000000", fill = "#b3b3f9", na.rm=TRUE,  center=0)+ xlim(0,9) + ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("Low (TioLi)")

p2<-ggplot(subset(data,urn=="Middle" & t>10 & role=="Seller"& delegation==FALSE & chat==FALSE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth =1, center=0 , color = "#000000", fill = "#b3b3f9", na.rm=TRUE)+xlim(0,9)+ ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("Middle (TioLi)")

p3<-ggplot(subset(data,urn=="High" & t>10 & role=="Seller"& delegation==FALSE & chat==FALSE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth=1, center=0 ,color = "#000000", fill = "#b3b3f9", na.rm=TRUE)+xlim(0,9)+ ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("High (TioLi)")

p4 <-ggplot(subset(data,urn=="Low" & t>10 & role=="Seller" & delegation==TRUE & chat==FALSE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth =1,color = "#000000", fill = "#b3b3f9", na.rm=TRUE,  center=0)+ xlim(0,9) + ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("Low (Dele)")

p5<-ggplot(subset(data,urn=="Middle" & t>10 & role=="Seller"& delegation==TRUE & chat==FALSE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth =1, center=0 , color = "#000000", fill = "#b3b3f9", na.rm=TRUE)+xlim(0,9)+ ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("Middle (Dele)")

p6<-ggplot(subset(data,urn=="High" & t>10 & role=="Seller"& delegation==TRUE & chat==FALSE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth=1, center=0 ,color = "#000000", fill = "#b3b3f9", na.rm=TRUE)+xlim(0,9)+ ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("High (Dele)")

DrawHist <- (p1 | p2 | p3)/(p4 | p5 | p6)
DrawHist



p1c <-ggplot(subset(data,urn=="Low" & t>10 & role=="Seller" & delegation==FALSE & chat==TRUE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth =1,color = "#000000", fill = "#b3b3f9", na.rm=TRUE,  center=0)+ xlim(0,9) + ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("Take-it-or-Leave-It: Low")

p2c <-ggplot(subset(data,urn=="Middle" & t>10 & role=="Seller"& delegation==FALSE & chat==TRUE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth =1, center=0 , color = "#000000", fill = "#b3b3f9", na.rm=TRUE)+xlim(0,9)+ ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("Middle (TioLi)")

p3c <-ggplot(subset(data,urn=="High" & t>10 & role=="Seller"& delegation==FALSE & chat==TRUE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth=1, center=0 ,color = "#000000", fill = "#b3b3f9", na.rm=TRUE)+xlim(0,9)+ ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("High (TioLi)")

p4c <-ggplot(subset(data,urn=="Low" & t>10 & role=="Seller" & delegation==TRUE & chat==TRUE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth =1,color = "#000000", fill = "#b3b3f9", na.rm=TRUE,  center=0)+ xlim(0,9) + ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("Low (Dele)")

p5c <-ggplot(subset(data,urn=="Middle" & t>10 & role=="Seller"& delegation==TRUE & chat==TRUE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth =1, center=0 , color = "#000000", fill = "#b3b3f9", na.rm=TRUE)+xlim(0,9)+ ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("Middle (Dele)")

p6c <-ggplot(subset(data,urn=="High" & t>10 & role=="Seller"& delegation==TRUE & chat==TRUE), aes(x=minX, y= after_stat(count / sum(count)))) + 
  geom_histogram(position="identity",binwidth=1, center=0 ,color = "#000000", fill = "#b3b3f9", na.rm=TRUE)+xlim(0,9)+ ylim(0,0.5) +
  xlab('Min offer')+ylab('Proportion')+ggtitle("High (Dele)")

DrawHistc <- (p1c | p2c | p3c)/(p4c | p5c | p6c)
DrawHistc

##### Offers: Display plots #####

#### No Chat ####

# Theme for all plots

nice_blue <- "#4B9CD3"  # A clean, readable blue

nice_theme <- theme_classic(base_size = 12) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold", size = 13),
    axis.title = element_text(size = 11),
    axis.text = element_text(size = 10),
    axis.line = element_line(color = "black"),
    panel.grid.major.y = element_line(color = "gray90", size = 0.3),
    panel.grid.minor = element_blank()
  )

# Function to generate plots
make_offer_plot <- function(df, chat, delegation, urn_label) {
  df_plot <- df %>%
    filter(urn == urn_label, t > 10, role == "Seller",
           chat == !!chat, delegation == !!delegation) %>%
    count(minX) %>%
    mutate(prop = n / sum(n))
  
  label_main <- if (delegation) "Delegation" else "Take-it-or-Leave-It"
  y_label <- if (delegation) "Minimum Offer" else "Offer"
  title <- paste(label_main, ":", urn_label)
  
  ggplot(df_plot, aes(x = minX, y = prop)) +
    geom_col(fill = "#5DADE2", color = "black", width = 1) +
    scale_x_continuous(breaks = 0:9, limits = c(0, 9)) +
    scale_y_continuous(limits = c(0, 0.65)) +
    xlab(y_label) + ylab("Proportion") +
    ggtitle(title) + nice_theme
}

# Generate no-chat plots
p1 <- make_offer_plot(data, chat = FALSE, delegation = FALSE, urn_label = "Low")
p2 <- make_offer_plot(data, chat = FALSE, delegation = FALSE, urn_label = "Middle")
p3 <- make_offer_plot(data, chat = FALSE, delegation = FALSE, urn_label = "High")
p4 <- make_offer_plot(data, chat = FALSE, delegation = TRUE, urn_label = "Low")
p5 <- make_offer_plot(data, chat = FALSE, delegation = TRUE, urn_label = "Middle")
p6 <- make_offer_plot(data, chat = FALSE, delegation = TRUE, urn_label = "High")

DrawHist <- (p1 | p2 | p3) / (p4 | p5 | p6)
DrawHist

# Generate chat-enabled plots
p1c <- make_offer_plot(data, chat = TRUE, delegation = FALSE, urn_label = "Low")
p2c <- make_offer_plot(data, chat = TRUE, delegation = FALSE, urn_label = "Middle")
p3c <- make_offer_plot(data, chat = TRUE, delegation = FALSE, urn_label = "High")
p4c <- make_offer_plot(data, chat = TRUE, delegation = TRUE, urn_label = "Low")
p5c <- make_offer_plot(data, chat = TRUE, delegation = TRUE, urn_label = "Middle")
p6c <- make_offer_plot(data, chat = TRUE, delegation = TRUE, urn_label = "High")

DrawHistc <- (p1c | p2c | p3c) / (p4c | p5c | p6c)

# Display plots
DrawHist
DrawHistc

#### Accepted Offers ####

# Function for accepted offers (y)
make_accepted_plot <- function(df, chat, delegation, urn_label) {
  df_plot <- df %>%
    filter(urn == urn_label, t > 10, role == "Seller",
           chat == !!chat, delegation == !!delegation) %>%
    count(y) %>%
    mutate(prop = n / sum(n))
  
  label_main <- if (delegation) "Delegation" else "Take-it-or-Leave-It"
  y_label <- "Accepted Offer"
  title <- paste(label_main, ":", urn_label)
  
  ggplot(df_plot, aes(x = y, y = prop)) +
    geom_col(fill = "#117A65", color = "black", width = 1) +
    scale_x_continuous(breaks = 0:9, limits = c(0, 9)) +
    scale_y_continuous(limits = c(0, 0.7)) +
    xlab(y_label) + ylab("Proportion") +
    ggtitle(title) + nice_theme
}

# Generate plots: Accepted offers, no chat
a1 <- make_accepted_plot(data, chat = FALSE, delegation = FALSE, urn_label = "Low")
a2 <- make_accepted_plot(data, chat = FALSE, delegation = FALSE, urn_label = "Middle")
a3 <- make_accepted_plot(data, chat = FALSE, delegation = FALSE, urn_label = "High")
a4 <- make_accepted_plot(data, chat = FALSE, delegation = TRUE, urn_label = "Low")
a5 <- make_accepted_plot(data, chat = FALSE, delegation = TRUE, urn_label = "Middle")
a6 <- make_accepted_plot(data, chat = FALSE, delegation = TRUE, urn_label = "High")

DrawHistAccepted <- (a1 | a2 | a3) / (a4 | a5 | a6)

# Display
DrawHistAccepted

# Function for accepted offers (chat condition)
make_accepted_plot <- function(df, chat, delegation, urn_label) {
  df_plot <- df %>%
    filter(urn == urn_label, t > 10, role == "Seller",
           chat == !!chat, delegation == !!delegation) %>%
    count(y) %>%
    mutate(prop = n / sum(n))
  
  label_main <- if (delegation) "Delegation" else "Take-it-or-Leave-It"
  y_label <- "Accepted Offer"
  title <- paste(label_main, ":", urn_label)
  
  ggplot(df_plot, aes(x = y, y = prop)) +
    geom_col(fill = "#117A65", color = "black", width = 1) +
    scale_x_continuous(breaks = 0:9, limits = c(0, 9)) +
    scale_y_continuous(limits = c(0, 0.7)) +
    xlab(y_label) + ylab("Proportion") +
    ggtitle(title) + nice_theme
}

# Generate plots: Accepted offers, chat condition
a1c <- make_accepted_plot(data, chat = TRUE, delegation = FALSE, urn_label = "Low")
a2c <- make_accepted_plot(data, chat = TRUE, delegation = FALSE, urn_label = "Middle")
a3c <- make_accepted_plot(data, chat = TRUE, delegation = FALSE, urn_label = "High")
a4c <- make_accepted_plot(data, chat = TRUE, delegation = TRUE, urn_label = "Low")
a5c <- make_accepted_plot(data, chat = TRUE, delegation = TRUE, urn_label = "Middle")
a6c <- make_accepted_plot(data, chat = TRUE, delegation = TRUE, urn_label = "High")

DrawHistAcceptedChat <- (a1c | a2c | a3c) / (a4c | a5c | a6c)

# Display
DrawHistAcceptedChat



#### Overlay Plots ####

# Function for overlay histograms (no chat condition)
make_overlay_plot <- function(df, delegation, urn_label) {
  df_filtered <- df %>%
    filter(urn == urn_label, t > 10, role == "Seller",
           chat == FALSE, delegation == !!delegation)
  
  df_offers <- df_filtered %>%
    count(minX) %>%
    mutate(prop = n / sum(n), type = "Offer", x = minX)
  
  df_accepts <- df_filtered %>%
    count(y) %>%
    mutate(prop = n / sum(n), type = "Accepted", x = y)
  
  df_plot <- bind_rows(df_offers, df_accepts)
  
  label_main <- if (delegation) "Delegation" else "Take-it-or-Leave-It"
  title <- paste(label_main, ":", urn_label)
  x_label <- if (delegation) "Minimum Offer" else "Offer"
  
  ggplot(df_plot, aes(x = x, y = prop, fill = type)) +
    geom_col(position = "identity", width = 0.8, color = "black", alpha = 0.7) +
    scale_fill_manual(values = c("Offer" = "#b3b3f9", "Accepted" = "#117A65")) +
    scale_x_continuous(breaks = 0:9, limits = c(0, 9)) +
    scale_y_continuous(limits = c(0, 0.7)) +
    xlab(x_label) + ylab("Proportion") +
    ggtitle(title) +
    nice_theme +
    guides(fill = guide_legend(title = NULL))
}

# Create 6 overlay plots for no-chat condition
ov1 <- make_overlay_plot(data, delegation = FALSE, urn_label = "Low")
ov2 <- make_overlay_plot(data, delegation = FALSE, urn_label = "Middle")
ov3 <- make_overlay_plot(data, delegation = FALSE, urn_label = "High")
ov4 <- make_overlay_plot(data, delegation = TRUE, urn_label = "Low")
ov5 <- make_overlay_plot(data, delegation = TRUE, urn_label = "Middle")
ov6 <- make_overlay_plot(data, delegation = TRUE, urn_label = "High")

# Combine plots
DrawOverlayHist <- (ov1 | ov2 | ov3) / (ov4 | ov5 | ov6)

# Display
DrawOverlayHist


# Overlay plot function (chat condition)
make_overlay_plot <- function(df, delegation, urn_label) {
  df_filtered <- df %>%
    filter(urn == urn_label, t > 10, role == "Seller",
           chat == TRUE, delegation == !!delegation)
  
  df_offers <- df_filtered %>%
    count(minX) %>%
    mutate(prop = n / sum(n), type = "Offer", x = minX)
  
  df_accepts <- df_filtered %>%
    count(y) %>%
    mutate(prop = n / sum(n), type = "Accepted", x = y)
  
  df_plot <- bind_rows(df_offers, df_accepts)
  
  label_main <- if (delegation) "Delegation" else "Take-it-or-Leave-It"
  title <- paste(label_main, ":", urn_label)
  x_label <- if (delegation) "Minimum Offer" else "Offer"
  
  ggplot(df_plot, aes(x = x, y = prop, fill = type)) +
    geom_col(position = "identity", width = 0.8, color = "black", alpha = 0.7) +
    scale_fill_manual(values = c("Offer" = "#b3b3f9", "Accepted" = "#117A65")) +
    scale_x_continuous(breaks = 0:9, limits = c(0, 9)) +
    scale_y_continuous(limits = c(0, 0.7)) +
    xlab(x_label) + ylab("Proportion") +
    ggtitle(title) +
    nice_theme +
    guides(fill = guide_legend(title = NULL))
}

# Create 6 plots for chat condition
ov1c <- make_overlay_plot(data, delegation = FALSE, urn_label = "Low")
ov2c <- make_overlay_plot(data, delegation = FALSE, urn_label = "Middle")
ov3c <- make_overlay_plot(data, delegation = FALSE, urn_label = "High")
ov4c <- make_overlay_plot(data, delegation = TRUE, urn_label = "Low")
ov5c <- make_overlay_plot(data, delegation = TRUE, urn_label = "Middle")
ov6c <- make_overlay_plot(data, delegation = TRUE, urn_label = "High")

# Combine
DrawOverlayHistChat <- (ov1c | ov2c | ov3c) / (ov4c | ov5c | ov6c)

# Display
DrawOverlayHistChat

# Compare chat to no chat tioli

DrawOverlayChatTioli <- (ov1 | ov2 | ov3) / (ov1c | ov2c | ov3c)
DrawOverlayChatTioli

DrawOverlayChatDel <- (ov4 | ov5 | ov6) / (ov4c | ov5c | ov6c)
DrawOverlayChatDel

#### Cummulative offers in Delegation ####


# Helper function to compute proportions of values available in [minX:maxX]
get_value_availability <- function(df, urn_label, chat_cond) {
  df_filtered <- df %>%
    filter(
      delegation == TRUE,
      role == "Seller",
      t > 10,
      urn == urn_label,
      chat == chat_cond
    ) %>%
    select(i, t, minX, maxX)
  
  total_offers <- nrow(df_filtered)
  
  expanded <- df_filtered %>%
    rowwise() %>%
    mutate(offer_values = list(minX:maxX)) %>%
    unnest(offer_values) %>%
    ungroup() %>%
    distinct(i, t, offer_values) %>%
    count(offer_values) %>%
    mutate(proportion = n / total_offers)
  
  # Fill missing values from 0 to 9 with 0
  full <- tibble(offer_values = 0:9) %>%
    left_join(expanded, by = "offer_values") %>%
    mutate(proportion = replace_na(proportion, 0))
  
  return(full)
}

# Generate 6 datasets
plot_data <- list(
  low_nochat  = get_value_availability(data, "Low", FALSE),
  mid_nochat  = get_value_availability(data, "Middle", FALSE),
  high_nochat = get_value_availability(data, "High", FALSE),
  low_chat    = get_value_availability(data, "Low", TRUE),
  mid_chat    = get_value_availability(data, "Middle", TRUE),
  high_chat   = get_value_availability(data, "High", TRUE)
)

# Plotting function
make_availability_plot <- function(df, title) {
  ggplot(df, aes(x = offer_values, y = proportion)) +
    geom_col(fill = "#117A65", color = "black", width = 0.8) +
    scale_x_continuous(breaks = 0:9, limits = c(0, 9)) +
    scale_y_continuous(limits = c(0, 1)) +
    xlab("Value Offered") + ylab("Proportion of Offers Including Value") +
    ggtitle(title) +
    nice_theme
}

# Generate plots
p1 <- make_availability_plot(plot_data$low_nochat, "Low Urn (No Chat)")
p2 <- make_availability_plot(plot_data$mid_nochat, "Middle Urn (No Chat)")
p3 <- make_availability_plot(plot_data$high_nochat, "High Urn (No Chat)")
p4 <- make_availability_plot(plot_data$low_chat, "Low Urn (Chat)")
p5 <- make_availability_plot(plot_data$mid_chat, "Middle Urn (Chat)")
p6 <- make_availability_plot(plot_data$high_chat, "High Urn (Chat)")

# Combine with patchwork
DelegationValueAvailability <- (p1 | p2 | p3) / (p4 | p5 | p6)

# Show all
DelegationValueAvailability

#### Delegation: Accepted offers out of all available #### 

# Helper function to compute proportions of availability and acceptance
get_overlay_data <- function(df, urn_label, chat_cond) {
  df_filtered <- df %>%
    filter(
      delegation == TRUE,
      role == "Seller",
      t > 10,
      urn == urn_label,
      chat == chat_cond
    ) %>%
    select(i, t, minX, maxX, y)
  
  total_offers <- nrow(df_filtered)
  
  # Expand [minX:maxX] values
  available <- df_filtered %>%
    rowwise() %>%
    mutate(offer_values = list(minX:maxX)) %>%
    unnest(offer_values) %>%
    ungroup() %>%
    distinct(i, t, offer_values) %>%
    count(offer_values) %>%
    mutate(avail_prop = n / total_offers)
  
  # Accepted offers (y)
  accepted <- df_filtered %>%
    count(y) %>%
    rename(offer_values = y, accepted_n = n) %>%
    mutate(acc_prop = accepted_n / total_offers)
  
  # Merge and fill missing values
  full <- tibble(offer_values = 0:9) %>%
    left_join(available, by = "offer_values") %>%
    left_join(accepted, by = "offer_values") %>%
    mutate(
      avail_prop = replace_na(avail_prop, 0),
      acc_prop   = replace_na(acc_prop, 0)
    )
  
  return(full)
}

# Plot function
make_overlay_plot <- function(df, title) {
  ggplot(df, aes(x = offer_values)) +
    geom_col(aes(y = avail_prop), fill = "#117A65", color = "black", width = 0.8) +
    geom_line(aes(y = acc_prop), color = "black", size = 1.1) +
    geom_point(aes(y = acc_prop), color = "black", size = 2) +
    scale_x_continuous(breaks = 0:9, limits = c(0, 9)) +
    scale_y_continuous(limits = c(0, 1)) +
    xlab("Value") + ylab("Proportion") +
    ggtitle(title) +
    nice_theme
}

# Generate 6 datasets
overlay_data <- list(
  low_nochat  = get_overlay_data(data, "Low", FALSE),
  mid_nochat  = get_overlay_data(data, "Middle", FALSE),
  high_nochat = get_overlay_data(data, "High", FALSE),
  low_chat    = get_overlay_data(data, "Low", TRUE),
  mid_chat    = get_overlay_data(data, "Middle", TRUE),
  high_chat   = get_overlay_data(data, "High", TRUE)
)

# Plot function: gray bar for availability, green bar for accepted
make_overlay_bar_plot <- function(df, title) {
  ggplot(df, aes(x = offer_values)) +
    geom_col(aes(y = avail_prop), fill = "#D5D8DC", color = "black", width = 0.8) +
    geom_col(aes(y = acc_prop), fill = "#117A65", width = 0.5) +
    scale_x_continuous(breaks = 0:9, limits = c(0, 9)) +
    scale_y_continuous(limits = c(0, 1)) +
    xlab("Value") + ylab("Proportion") +
    ggtitle(title) +
    nice_theme
}

# Regenerate overlay plots
p1g <- make_overlay_bar_plot(overlay_data$low_nochat, "Low Urn (No Chat)")
p2g <- make_overlay_bar_plot(overlay_data$mid_nochat, "Middle Urn (No Chat)")
p3g <- make_overlay_bar_plot(overlay_data$high_nochat, "High Urn (No Chat)")
p4g <- make_overlay_bar_plot(overlay_data$low_chat, "Low Urn (Chat)")
p5g <- make_overlay_bar_plot(overlay_data$mid_chat, "Middle Urn (Chat)")
p6g <- make_overlay_bar_plot(overlay_data$high_chat, "High Urn (Chat)")

# Combine with patchwork
OverlayBarCharts <- (p1g | p2g | p3g) / (p4g | p5g | p6g)

# Show
OverlayBarCharts



#### Seller Payoffs ####



seller_data <- data %>%
  filter(role == "Seller" & t>5 ) %>%
  group_by(delegation, chat, urn) %>%
  summarise(
    n = n(),
    avg.widgets = round(mean(y),3),
    ,.groups = 'drop') %>%
  ungroup()

seller_data$Mech <- ifelse(seller_data$delegation, "Delegation", "TIOLI")
seller_data$Comm <- ifelse(seller_data$chat, "Chat", "NoChat")

seller_data <- pivot_wider(seller_data[, c("Mech","Comm",'urn','avg.widgets')], names_from = urn, values_from = avg.widgets)

seller_data[, c("Mech","Comm",'Low','Middle','High')]

late.seller <- subset(data,t>5 & role == "Seller")
late.seller$dist<-as.factor(late.seller$urn)

y.out <- lm_robust( y ~  dist*delegation*chat, data= late.seller, cluster=i)

summary(y.out)


new.data <- expand.grid(
  dist = as.factor(c("Low", "Middle", "High")),
  delegation = c(TRUE, FALSE),
  chat = c(TRUE, FALSE)
)

prediction <- prediction(y.out, data = new.data)
prediction


#### Breakdown Graphs ####

breakdown_data <- data %>%
  filter(role == "Buyer", t > 10) %>%
  group_by(delegation, chat, urn) %>%
  summarise(
    n = n(),
    breakdowns = sum(y == 0),
    breakdowns_rate = mean(y == 0),
    inefficiencies = sum(y < theta, na.rm = TRUE),
    inefficiency_rate = mean(y < theta, na.rm = TRUE),
    .groups = "drop"
  )
breakdown_data$urn <- factor(breakdown_data$urn, levels = c("High", "Middle", "Low"))

breakdown_data$Mech <- ifelse(breakdown_data$delegation, "Delegation", "TIOLI")
breakdown_data$Comm <- ifelse(breakdown_data$chat, "Chat", "NoChat")

breakdown_table <- pivot_wider(breakdown_data[, c("Mech","Comm",'urn','breakdowns_rate')], names_from = urn, values_from = breakdowns_rate)

ineff_table<- pivot_wider(breakdown_data[, c("Mech","Comm",'urn','inefficiency_rate')], names_from = urn, values_from = inefficiency_rate)

ineff_table[, c("Mech","Comm",'Low','Middle','High')]

breakdown_table[, c("Mech","Comm",'Low','Middle','High')]

ggplot(breakdown_table, aes(x = interaction(Mech, Comm), y = High)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  labs(
    title = "Breakdown Rate by Treatment",
    x = "Treatment (Delegation × Chat)",
    y = "Fraction of Breakdowns (y = 0)",
    caption = "Only includes decisions where role == 'Buyer'"
  ) +
  scale_x_discrete(labels = function(x) {
    sapply(strsplit(as.character(x), "\\."), function(p) {
      paste0(p[1], "\n", p[2])
    })
  }) +
  theme_minimal()

ggplot(breakdown_data, aes(x = interaction(Mech, Comm), y = breakdowns_rate, fill = urn)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(
    title = "Breakdown Rate by Treatment and Urn",
    x = "Treatment (Delegation × Chat)",
    y = "Breakdown Rate (y = 0)",
    fill = "Urn Type"
  ) +
  theme_minimal(base_size = 12)


# Reshape the inefficiency data to long format
ineff_long <- breakdown_table[, c("Mech", "Comm", "Low", "Middle", "High")] %>%
  pivot_longer(cols = c("Low", "Middle", "High"),
               names_to = "Urn", values_to = "Inefficiency") %>%
  mutate(Urn = factor(Urn, levels = c("High", "Middle", "Low")))

# Bar plot
ggplot(ineff_long, aes(x = Urn, y = Inefficiency, fill = Comm)) +
  geom_bar(stat = "identity", position = position_dodge(), width = 0.7) +
  facet_wrap(~Mech) +
  scale_fill_manual(values = c("NoChat" = "gray60", "Chat" = "darkseagreen3")) +
  labs(
    title = "Inefficiency by Urn, Communication, and Mechanism",
    x = "Urn Type",
    y = "Inefficiency Rate",
    fill = "Communication"
  ) +
  theme_minimal(base_size = 13)

#### Surplus ####


data <- data %>%
  mutate(
    seller_surplus = ifelse(role == "Seller", (y - theta) / (8 - theta), NA_real_)
  )

# Unconditional 
avg_surplus <- data %>%
  filter(role == "Seller", t > 10) %>%  # Focus on Sellers and final 10 rounds
  group_by(delegation, chat) %>%
  summarise(
    avg_surplus = mean(seller_surplus, na.rm = TRUE),
    n = n(),
    .groups = "drop"
  ) %>%
  mutate(
    Mech = ifelse(delegation, "Delegation", "TIOLI"),
    Comm = ifelse(chat, "Chat", "NoChat")
  ) %>%
  select(Mech, Comm, avg_surplus, n)
avg_surplus

# Conditional on no breakdown
avg_surplus <- data %>%
  filter(role == "Seller", t > 10, y > 0) %>%  # Only accepted offers
  group_by(delegation, chat) %>%
  summarise(
    avg_surplus = mean(seller_surplus, na.rm = TRUE),
    n = n(),
    .groups = "drop"
  ) %>%
  mutate(
    Mech = ifelse(delegation, "Delegation", "TIOLI"),
    Comm = ifelse(chat, "Chat", "NoChat")
  ) %>%
  select(Mech, Comm, avg_surplus, n)
avg_surplus 

avg_surplus_efficient <- data %>%
  filter(role == "Seller", t > 10, y >= theta) %>%  # Only efficient accepted offers
  group_by(delegation, chat) %>%
  summarise(
    avg_surplus = mean(seller_surplus, na.rm = TRUE),
    n = n(),
    .groups = "drop"
  ) %>%
  mutate(
    Mech = ifelse(delegation, "Delegation", "TIOLI"),
    Comm = ifelse(chat, "Chat", "NoChat")
  ) %>%
  select(Mech, Comm, avg_surplus, n)
avg_surplus_efficient

# Combined conditional efficiency and surplus on non-breakdowns

library(ggrepel)  # For clear text labels

# 1. Efficiency rate among non-breakdowns
efficiency_rates_nb <- data %>%
  filter(role == "Buyer", t > 10) %>%
  group_by(delegation, chat) %>%
  summarise(
    efficiency_rate = mean(y >= theta, na.rm = TRUE),
    .groups = "drop"
  )

# 2. Seller surplus for efficient outcomes among non-breakdowns
avg_surplus_nb <- data %>%
  filter(role == "Seller", t > 10, y > 0) %>%
  group_by(delegation, chat) %>%
  summarise(
    avg_surplus = mean(seller_surplus, na.rm = TRUE),
    .groups = "drop"
  )

# 3. Combine
combined_nb <- left_join(efficiency_rates_nb, avg_surplus_nb, by = c("delegation", "chat")) %>%
  mutate(
    Mech = ifelse(delegation, "Delegation", "TIOLI"),
    Comm = ifelse(chat, "Chat", "NoChat")
  ) %>%
  select(Mech, Comm, efficiency_rate, avg_surplus)

ggplot(combined_nb, aes(x = efficiency_rate, y = avg_surplus, label = paste(Mech, Comm, sep = " - "))) +
  geom_point(size = 3, color = "darkblue") +
  geom_text_repel(size = 4, max.overlaps = Inf) +
  labs(
    title = "Seller Surplus vs. Efficiency (Non-Breakdown Outcomes Only)",
    x = "Efficiency Rate (y ≥ θ | y > 0)",
    y = "Average Seller Surplus (Non-Breakdown)"
  ) +
  xlim(0, 1) + ylim(0, 1) +
  theme_classic(base_size = 13)


# Combined conditional efficiency and surplus on efficient outcomes

# 1. Efficiency rate: proportion of efficient outcomes
efficiency_rates <- data %>%
  filter(role == "Buyer", t > 10) %>%
  group_by(delegation, chat) %>%
  summarise(
    efficiency_rate = mean(y >= theta, na.rm = TRUE),
    .groups = "drop"
  )

# 2. Seller surplus for efficient outcomes
avg_surplus_efficient <- data %>%
  filter(role == "Seller", t > 10, y >= theta) %>%
  group_by(delegation, chat) %>%
  summarise(
    avg_surplus = mean(seller_surplus, na.rm = TRUE),
    .groups = "drop"
  )

# 3. Combine and label
combined_summary <- left_join(efficiency_rates, avg_surplus_efficient, by = c("delegation", "chat")) %>%
  mutate(
    Mech = ifelse(delegation, "Delegation", "TIOLI"),
    Comm = ifelse(chat, "Chat", "NoChat")
  ) %>%
  select(Mech, Comm, efficiency_rate, avg_surplus)
combined_summary

# Scatterplot: Efficiency vs. Surplus
ggplot(combined_summary, aes(x = efficiency_rate, y = avg_surplus, label = paste(Mech, Comm, sep = " - "))) +
  geom_point(size = 3, color = "darkgreen") +
  geom_text_repel(size = 4, max.overlaps = Inf) +
  labs(
    title = "Seller Surplus vs. Efficiency Rate by Treatment",
    x = "Efficiency Rate (y ≥ θ)",
    y = "Average Seller Surplus (Efficient Outcomes Only)"
  ) +
  xlim(0, 1) + ylim(0, 1) +
  theme_classic(base_size = 13)

#### Inefficiency Decomposition ####

ineff_decomp <- data %>%
  filter(role == "Buyer", t > 10) %>%
  group_by(delegation, chat) %>%
  summarise(
    total_n = n(),
    breakdowns = sum(y == 0),
    suboptimal_choices = sum(y > 0 & y < theta, na.rm = TRUE),
    efficient_choices = sum(y >= theta, na.rm = TRUE),
    
    breakdown_rate = breakdowns / total_n,
    suboptimal_rate = suboptimal_choices / total_n,
    efficiency_rate = efficient_choices / total_n,
    
    .groups = "drop"
  ) %>%
  mutate(
    Mech = ifelse(delegation, "Delegation", "TIOLI"),
    Comm = ifelse(chat, "Chat", "NoChat")
  ) %>%
  select(Mech, Comm, breakdown_rate, suboptimal_rate, efficiency_rate)

# Reshape for plotting
ineff_long <- ineff_decomp %>%
  pivot_longer(cols = c(breakdown_rate, suboptimal_rate, efficiency_rate),
               names_to = "Outcome", values_to = "Rate")

ggplot(ineff_long, aes(x = interaction(Mech, Comm), y = Rate, fill = Outcome)) +
  geom_bar(stat = "identity") +
  scale_fill_manual(
    values = c(
      "efficiency_rate" = "#1b9e77",      # Teal Green
      "suboptimal_rate" = "#d95f02",      # Muted Orange
      "breakdown_rate"  = "#7570b3"       # Dusty Purple
    ),
    labels = c(
      "efficiency_rate" = "Efficient (y ≥ θ)",
      "suboptimal_rate" = "Suboptimal (0 < y < θ)",
      "breakdown_rate"  = "Breakdown (y = 0)"
    )
  ) +
  labs(
    title = "Decomposition of Buyer Decisions by Treatment",
    x = "Treatment",
    y = "Proportion of Rounds",
    fill = "Decision Outcome"
  ) +
  theme_classic(base_size = 13) +
  scale_x_discrete(labels = function(x) gsub("\\.", "\n", x))

# Urn-type efficiency

# Filter to non-breakdown outcomes only
non_breakdown_data <- data %>%
  filter(role == "Buyer", t > 10, y > 0)

# Compute efficiency and surplus by Mech, Comm, and urn
efficiency_surplus_colored <- data %>%
  filter(role == "Buyer", t > 10, y > 0) %>%
  mutate(
    surplus = (y - theta) / (8 - theta),
    Mech = ifelse(delegation, "Delegation", "TIOLI"),
    Comm = ifelse(chat, "Chat", "NoChat")
  ) %>%
  group_by(Mech, Comm, urn) %>%
  summarise(
    efficiency = mean(y >= theta),
    avg_surplus = mean(surplus, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  mutate(
    urn = factor(urn, levels = c("Low", "Middle", "High")),  # Order the urn factor
    label = paste(Mech, Comm, urn, sep = " - ")
  )

# Create a shape label column
efficiency_surplus_colored <- efficiency_surplus_colored %>%
  mutate(
    mech_comm = paste(Mech, Comm, sep = " – ")
  )

# Define shape types (up to 6 unique combinations)
mech_comm_shapes <- c(
  "TIOLI – NoChat"    = 16,  # filled circle
  "TIOLI – Chat"      = 17,  # filled triangle
  "Delegation – NoChat" = 15,  # filled square
  "Delegation – Chat"   = 18   # filled diamond
)


# Color palette for urn types
urn_colors <- c(
  "Low" = "#d95f02",     # muted orange
  "Middle" = "#1b9e77",  # teal green
  "High" = "#7570b3"     # dusty purple
)

# Plot
ggplot(efficiency_surplus_colored, aes(x = efficiency, y = avg_surplus, color = urn, shape = mech_comm, label = label)) +
  geom_point(size = 3.5) +
  geom_text_repel(size = 3.5, max.overlaps = 20, show.legend = FALSE) +
  scale_color_manual(values = urn_colors) +
  scale_shape_manual(values = mech_comm_shapes) +
  labs(
    x = "Efficiency Rate (y ≥ θ)",
    y = "Average Seller Surplus",
    title = "Efficiency vs Seller Surplus by Treatment and Urn",
    color = "Urn Type",
    shape = "Mech – Comm"
  ) +
  theme_minimal(base_size = 13)

# Urn-type efficiency

# Filter to non-breakdown outcomes only
non_breakdown_data <- data %>%
  filter(role == "Buyer", t > 10)

# Compute efficiency and surplus by Mech, Comm, and urn
efficiency_surplus_colored <- data %>%
  filter(role == "Buyer", t > 10) %>%
  mutate(
    surplus = (y - theta) / (8 - theta),
    Mech = ifelse(delegation, "Delegation", "TIOLI"),
    Comm = ifelse(chat, "Chat", "NoChat")
  ) %>%
  group_by(Mech, Comm, urn) %>%
  summarise(
    efficiency = mean(y >= theta),
    avg_surplus = mean(surplus, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  mutate(
    urn = factor(urn, levels = c("Low", "Middle", "High")),  # Order the urn factor
    label = paste(Mech, Comm, urn, sep = " - ")
  )

# Create a shape label column
efficiency_surplus_colored <- efficiency_surplus_colored %>%
  mutate(
    mech_comm = paste(Mech, Comm, sep = " – ")
  )

# Define shape types (up to 6 unique combinations)
mech_comm_shapes <- c(
  "TIOLI – NoChat"    = 16,  # filled circle
  "TIOLI – Chat"      = 17,  # filled triangle
  "Delegation – NoChat" = 15,  # filled square
  "Delegation – Chat"   = 18   # filled diamond
)


# Color palette for urn types
urn_colors <- c(
  "Low" = "#d95f02",     # muted orange
  "Middle" = "#1b9e77",  # teal green
  "High" = "#7570b3"     # dusty purple
)

# Plot
ggplot(efficiency_surplus_colored, aes(x = efficiency, y = avg_surplus, color = urn, shape = mech_comm, label = label)) +
  geom_point(size = 3.5) +
  geom_text_repel(size = 3.5, max.overlaps = 20, show.legend = FALSE) +
  scale_color_manual(values = urn_colors) +
  scale_shape_manual(values = mech_comm_shapes) +
  labs(
    x = "Efficiency Rate (y ≥ θ)",
    y = "Average Seller Surplus",
    title = "Efficiency vs Seller Surplus by Treatment and Urn",
    color = "Urn Type",
    shape = "Mech – Comm"
  ) +
  theme_classic(base_size = 13)

# Urn-type efficiency

# Filter to non-breakdown outcomes only
non_breakdown_data <- data %>%
  filter(role == "Buyer", t > 10, y > 0)

# Compute efficiency and surplus by Mech, Comm, and urn
efficiency_surplus_colored <- data %>%
  filter(role == "Buyer", t > 10, y > 0) %>%
  mutate(
    surplus = (y - theta) / (8 - theta),
    Mech = ifelse(delegation, "Delegation", "TIOLI"),
    Comm = ifelse(chat, "Chat", "NoChat")
  ) %>%
  group_by(Mech, Comm, urn) %>%
  summarise(
    efficiency = mean(y >= theta),
    avg_surplus = mean(surplus, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  mutate(
    urn = factor(urn, levels = c("Low", "Middle", "High")),  # Order the urn factor
    label = paste(Mech, Comm, urn, sep = " - ")
  )

# Create a shape label column
efficiency_surplus_colored <- efficiency_surplus_colored %>%
  mutate(
    mech_comm = paste(Mech, Comm, sep = " – ")
  )

# Define shape types (up to 6 unique combinations)
mech_comm_shapes <- c(
  "TIOLI – NoChat"    = 16,  # filled circle
  "TIOLI – Chat"      = 17,  # filled triangle
  "Delegation – NoChat" = 15,  # filled square
  "Delegation – Chat"   = 18   # filled diamond
)


# Color palette for urn types
urn_colors <- c(
  "Low" = "#d95f02",     # muted orange
  "Middle" = "#1b9e77",  # teal green
  "High" = "#7570b3"     # dusty purple
)

# Plot
ggplot(efficiency_surplus_colored, aes(x = efficiency, y = avg_surplus, color = urn, shape = mech_comm, label = label)) +
  geom_point(size = 3.5) +
  geom_text_repel(size = 3.5, max.overlaps = 20, show.legend = FALSE) +
  scale_color_manual(values = urn_colors) +
  scale_shape_manual(values = mech_comm_shapes) +
  labs(
    x = "Efficiency Rate (y ≥ θ)",
    y = "Average Seller Surplus",
    title = "Efficiency vs Seller Surplus by Treatment and Urn",
    color = "Urn Type",
    shape = "Mech – Comm"
  ) +
  theme_classic(base_size = 13)


