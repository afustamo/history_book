library(ggplot2)

# Initialize an empty data frame to store character information
characters <- data.frame(
  name = character(),
  date_of_birth = character(),
  date_of_death = character(),
  stringsAsFactors = FALSE
)

# Function to add a new character
add_character <- function() {
  cat("Enter the details for the new character:\n")
  name <- readline(prompt = "Name: ")
  birth_date <- readline(prompt = "Date of Birth (YYYY/MM/DD): ")
  death_date <- readline(prompt = "Date of Death (Leave blank if alive): ")

  # Add the new character to the data frame
  new_character <- data.frame(
    name = name,
    date_of_birth = birth_date,
    date_of_death = ifelse(death_date == "", NA, death_date),
    stringsAsFactors = FALSE
  )
  characters <<- rbind(characters, new_character)
  cat("Character added successfully!\n")
}

# Function to modify an existing character
modify_character <- function() {
  cat("Enter the name of the character to modify: ")
  char_name <- readline()

  # Check if the character exists
  if (char_name %in% characters$name) {
    cat("Enter the new details for the character:\n")
    birth_date <- readline(prompt = "New Date of Birth (YYYY/MM/DD): ")
    death_date <- readline(prompt = "New Date of Death (Leave blank if alive): ")

    # Update the character in the data frame
    characters[characters$name == char_name, "date_of_birth"] <- birth_date
    characters[characters$name == char_name, "date_of_death"] <- ifelse(death_date == "", NA, death_date)
    cat("Character modified successfully!\n")
  } else {
    cat("Character not found.\n")
  }
}

# Function to display character information
display_character_info <- function() {
  cat("Enter the name of the character to display information: ")
  char_name <- readline()

  # Check if the character exists
  if (char_name %in% characters$name) {
    cat("Character Information:\n")
    print(characters[characters$name == char_name, ])
  } else {
    cat("Character not found.\n")
  }
}

# Function to display the map
display_map <- function() {
  ch2 <- characters
  ch2$date_of_death <- as.Date(ch2$date_of_death)
  ch2$date_of_death[is.na(ch2$date_of_death)]<-as.Date(Sys.Date())
  ggmap <- ggplot(ch2) +
    geom_segment(
      aes(
        y = name,
        yend = name,
        x = as.Date(date_of_birth),
        xend = as.Date(date_of_death),
        color = name  # Use the name for coloring
      ),
      linewidth = 3,  # Adjust the width of the segment
      show.legend = FALSE  # Hide the legend for geom_segment
    ) +
    geom_text(
      aes(
        y = name,
        x = as.Date((as.numeric(as.Date(date_of_birth)) + as.numeric(as.Date(date_of_death))) / 2),
        label = name
      ),
      vjust = 0,
      size = 3,  # Adjust the size of the text
      show.legend = FALSE  # Hide the legend for geom_text
    ) +
    scale_x_date(limits = c(as.Date("1800/1/1"), Sys.Date())) +
    scale_color_brewer(palette = "Pastel1") +  # Use a light color palette
    ggtitle("Historical Characters Map")
  rm(ch2)
  return(ggmap)
}


# Function to export the map (not implemented)
export_map <- function() {
  cat("Exporting the map (to be implemented).\n")
}


# Flag to control the game loop
exit_game <- FALSE
# Main game loop
# Main game loop
while (!exit_game) {
  cat("\nSelect an option:\n")
  cat("1: Add a character\n")
  cat("2: Modify an existing character\n")
  cat("3: Display character information\n")
  cat("4: Display the map\n")
  cat("5: Export the map\n")
  cat("0: Close\n")
  
  choice <- as.numeric(readline(prompt = "Enter your choice: "))
  
  if (choice == 1) {
    add_character()
  } else if (choice == 2) {
    modify_character()
  } else if (choice == 3) {
    display_character_info()
  } else if (choice == 4) {
    map <- display_map()
    print(map)
  } else if (choice == 5) {
    export_map()
  } else if (choice == 0) {
    cat("Closing the game. Goodbye!\n")
    exit_game <- TRUE  # Set the flag to exit the loop
  } else {
    cat("Invalid choice. Please enter a valid option.\n")
  }
}


