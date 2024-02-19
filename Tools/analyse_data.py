import pandas as pd

def aggregate_events_between_mains(input_file, output_file):

    # Daten einlesen
    df = pd.read_csv(input_file)

    # Neuen DataFrame für die aggregierten Daten vorbereiten
    aggregated_data = []

    # Variablen zur Zwischenspeicherung der Aggregation
    current_block = {}

    # Durch die Ereignisse iterieren
    for index, row in df.iterrows():
        label, duration = row['Label'], row['Duration (s)']

        # Neuen Block für 'Main' Ereignisse starten
        if label == 'Main':
            if current_block:  # Vorherigen Block speichern, falls vorhanden
                aggregated_data.append(current_block)
            current_block = {'Label': 'Main', 'Duration (s)': duration}
        else:
            # Ereignis zum aktuellen Block hinzufügen
            if label in current_block:
                current_block[label] += duration
            else:
                current_block[label] = duration

    # Letzten Block speichern
    if current_block:
        aggregated_data.append(current_block)

    # Aggregierte Daten in DataFrame umwandeln und in CSV speichern
    aggregated_df = pd.DataFrame(aggregated_data)
    aggregated_df.to_csv(output_file, index=False)

    return aggregated_df

input_file = '/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/timestamps.csv'
output_file = '/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/new.csv'

aggregate_events_between_mains(input_file, output_file)

