from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import re
from dicttoxml import dicttoxml


url = 'https://www.placardefutebol.com.br/'


def jogos_de_hoje(format='dict'):
    html = urlopen(url)
    page = BeautifulSoup(html, 'lxml')
    titles = page.find_all('h3', class_='match-list_league-name')
    championships = page.find_all('div', class_='container content')
    
    results = []
    
    for id, championship in enumerate(championships):
        matchs = championship.find_all('div', class_='row align-items-center content')
        
        for match in matchs:
            status = match.find('span', class_='status-name').text
            teams = match.find_all('div', class_='team-name')
            status = match.find('span', class_='status-name').text
            scoreboard = match.find_all('span', class_='badge badge-default')
            
            team_home = teams[0].text.strip()
            team_visitor = teams[1].text.strip()
            
            info = {
                'match': '{} x {}'.format(team_home, team_visitor),
                'status': status,
                'league': titles[id].text,
            }
            
            score = {}
            
            # Se o jogo já começou então existe placar.
            try:
                score['scoreboard'] = {
                    team_home: scoreboard[0].text,
                    team_visitor: scoreboard[1].text
                }
                score['summary'] = '{} x {}'.format(scoreboard[0].text, scoreboard[1].text)
            # Caso não tenha começado, armazena o horário de início
            except:
                score['start_in'] = status
                score['status'] = 'EM BREVE'
            
            info.update(score)
            
            results.append(info)
        
    if (format == 'json'):
        return json.dumps(results)
    elif (format == 'xml'):
        return dicttoxml(results)
    else:
        return results

  
def jogos_ao_vivo(format='dict'):
    matchs = jogos_de_hoje()
    results = list(filter(lambda match: re.findall(r'INTERVALO|AO VIVO|MIN', match['status']), matchs))
    
    if (format == 'json'):
        return json.dumps(results)
    elif (format == 'xml'):
        return dicttoxml(results)
    else:
        return results
        
def buscar_jogo_por_time(time):
    matchs = jogos_de_hoje()
    return list(filter(lambda match: time.lower() in match['match'].lower(), matchs))