# time_tracker.py

import os
import csv
import time
from datetime import datetime, timedelta
import pandas as pd

# Definições de constantes
TARGET_HOURS = 40

class TimeTracker:
    def __init__(self):
        pass

    def get_week_start_date(self, date=None):
        """Retorna a data de início da semana (segunda-feira) no formato ddmmyyyy."""
        if date is None:
            date = datetime.now()
        start_week = date - timedelta(days=date.weekday())  # Segunda-feira
        return start_week.strftime('%d%m%Y')

    def get_csv_filename(self):
        """Gera o nome do arquivo CSV com base na semana atual."""
        week_start_str = self.get_week_start_date()
        return f'weekly_hours_{week_start_str}.csv'

    def get_state_filename(self):
        """Gera o nome do arquivo de estado com base na semana atual."""
        week_start_str = self.get_week_start_date()
        return f'current_state_{week_start_str}.txt'

    def iniciar_timer(self, ticket):
        state_file = self.get_state_filename()
        if os.path.exists(state_file):
            return False, "Já existe um timer em execução. Por favor, encerre-o antes de iniciar um novo."
        start_time = time.time()
        with open(state_file, 'w') as f:
            f.write(f"{ticket},{start_time}")
        return True, f"Timer iniciado para o ticket {ticket} às {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}"

    def encerrar_timer(self):
        state_file = self.get_state_filename()
        if not os.path.exists(state_file):
            return False, "Nenhum timer está em execução."
        with open(state_file, 'r') as f:
            content = f.read().strip()
            if not content:
                return False, "Arquivo de estado vazio. Nenhum timer para encerrar."
            try:
                ticket, start_time = content.split(',')
                start_time = float(start_time)
            except ValueError:
                return False, "Formato do arquivo de estado inválido."
        end_time = time.time()
        elapsed_seconds = end_time - start_time

        if elapsed_seconds < 60:
            os.remove(state_file)
            return False, "O tempo registrado é inferior a 1 minuto. Nenhuma hora foi registrada."

        hours, remainder = divmod(int(elapsed_seconds), 3600)
        minutes = remainder // 60
        formatted_time = f"{hours}h {minutes}m"
        date_str = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d')
        csv_file = self.get_csv_filename()

        # Escreve no CSV
        self.write_to_csv(csv_file, ticket, date_str, formatted_time)

        # Remove o estado atual
        os.remove(state_file)
        status_message = f"Timer encerrado para o ticket {ticket} às {datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')}\nTempo registrado: {formatted_time}"
        status_message += "\n" + self.exibir_status()
        return True, status_message

    def write_to_csv(self, csv_file, ticket, date, hours):
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Ticket', 'Data', 'Horas']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({'Ticket': ticket, 'Data': date, 'Horas': hours})

    def exibir_status(self):
        csv_file = self.get_csv_filename()
        if not os.path.exists(csv_file):
            return "Nenhuma hora registrada ainda nesta semana."
        try:
            df = pd.read_csv(csv_file)
        except pd.errors.EmptyDataError:
            return "O arquivo CSV está vazio. Nenhuma hora registrada ainda."
        except Exception as e:
            return f"Ocorreu um erro ao ler o CSV: {e}"

        # Verifica se as colunas necessárias existem
        required_columns = {'Ticket', 'Data', 'Horas'}
        if not required_columns.issubset(df.columns):
            return f"O arquivo CSV está faltando uma ou mais colunas necessárias: {required_columns}"

        # Filtra para a semana atual (já que cada CSV é semanal, não é necessário filtrar novamente)
        current_week = df
        total_seconds = 0
        for time_str in current_week['Horas']:
            try:
                parts = time_str.replace('h', '').replace('m', '').split()
                h = int(parts[0])
                m = int(parts[1])
                total_seconds += h * 3600 + m * 60
            except (IndexError, ValueError):
                continue
        total_hours = total_seconds / 3600
        remaining = TARGET_HOURS - total_hours
        status = f"Horas realizadas nesta semana: {total_hours:.2f}h\n"
        if remaining > 0:
            status += f"Horas faltando para atingir {TARGET_HOURS}h semanais: {remaining:.2f}h"
        else:
            status += f"Você atingiu ou excedeu as {TARGET_HOURS} horas semanais!"
        return status
