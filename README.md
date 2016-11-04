# xStream für Kodi - Anleitung/ FAQ
- erweiterte/ umfangreiche User-Version
Erstellt für das Orignal xStream Forum 
http://xstream-addon.square7.ch/

![xStream logo](https://github.com/StoneOffStones/plugin.video.xstream/blob/wiki/graphics/website/logo/logo_512.png?raw=true)


- [1. Allgemeines zum Addon](#1-allgemeines-zum-addon)
    - [1.1 Verfügbare Webseiten](#11-verfügbare-webseiten)
    - [1.2 Rechtliche Konsequenzen bei Nutzung](#12-rechtliche-konsequenzen-bei-nutzung)
   
   
- [2. Installation und Konfiguration](#2-installation-und-konfiguration)
    - [2.1 Bezugsquellen zur Installation](#21-bezugsquellen-zur-installation)
    - [2.2 Allgemeine Einstellungen](#22-allgemeine-einstellungen)
    - [2.3 Webseiten Aktivieren und Deaktivieren](#23-webseiten-aktivieren-und-deaktivieren)
    - [2.4 Manuelle und automatische Hosterwahl](#24-manuelle-und-automatische-hosterwahl)
 - [2.5 Metahandler benutzen](#25-metahandler-benutzen)
 - [2.6 Autoplay Funktion](#26-autoplay-funktion)
 - [2.7 Zentralisierte Einstellungen](#27-zentralisierte-einstellungen)
 
- [3. Bekannte Probleme](#3-bekannte-probleme)
    - [3.1 Fehler bei der Installation](#31-fehler-bei-der-installation)
    - [3.2 Fehler bei Verwendung der Globalen Suche](#32-fehler-bei-verwendung-der-globalen-suche)
    - [3.3 Fehler bei Verwendung einzelner Webseiten](#33-fehler-bei-verwendung-einzelner-webseiten)
    - [3.4 URL Resolver Fehler](#34-url-resolver-fehler)
   - [3.5 Fehlermeldungen im Betrieb](#35-fehlermeldungen-im-betrieb)
  
- [4. Fehlerbericht über Log-Datei](#4-fehlerbericht-über-log-datei)
    - [4.1 Allgemeines zur Log-Datei](#41-allgemeines-zur-log-datei)
    - [4.2 Speicherort der Log Datei](#42-speicherort-der-log-datei)
    - [4.3 Erstellen und Hochladen der Log-Datei](#43-erstellen-und-hochladen-der-log-datei)

    
- [5. Phyton Dateien](#5-phyton-dateien)
    - [5.1 Allgemeines zur .py-Datei](#51-allgemeines-zur-py-datei)
    - [5.2 Bearbeiten einer .py-Datei](#52-bearbeiten-einer-py-datei)
    - [5.3 Speicherort der einzelnen Webseiten (.py Dateien)](#53-speicherort-der-einzelnen-webseiten-py-dateien)



## 1. Allgemeines zum Addon

xStream ist ein Video Addon für die Media-Center-Software Kodi. Mit xStream ist es möglich über eine simple Benutzeroberfläche mehrere Streaming-Seiten zu benutzen, mit denen man Filme und Serien anschauen kann.


### 1.1 Verfügbare Webseiten

| Name           | Domain            | Verfügbarkeit          | Stand      |
|:-------------- |:----------------- | :--------------------- | :--------- |
| AnimeLoads     | anime-loads.org   | funktioniert           | 09.04.2016 |
| BurningSeries  | bs.to             | funktioniert           | 09.04.2016 |
| Cine           | cine.to           | funktioniert           | 25.05.2016 |
| Cineplex       | cineplex.tv       | funktioniert           | 29.07.2016 |
| DirectDownLoad | ddl.me            | funktioniert           | 09.04.2016 |
| Dokustreamer   | dokustreamer.de   | funktioniert           | 28.08.2016 |
| Filmmerstube   | filmmerstube.com  | funktioniert           | 21.08.2016 |
| FilmPalast     | filmpalast.to     | funktioniert           | 09.04.2016 |
| FilmeStreamz   | filme-streamz.com | funktioniert           | 29.07.2016 |
| Goldstream     | goldstream.org    | funktioniert           | 23.06.2016 |
| HDfilme        | hdfilme.tv        | funktioniert           | 09.04.2016 |
| KinoKiste      | kkiste.to         | funktioniert teilweise | 09.04.2016 |
| KinoStreamz    | kino-streamz.com  | funktioniert           | 07.08.2016 |
| KinoX          | kinox.to          | funktioniert           | 09.04.2016 |
| Movie4k        | movie4k.to        | funktioniert           | 09.04.2016 |
| SerienStream   | serienstream.to   | funktioniert           | 26.10.2016 |
| MoviesEver     | moviesever.com    | funktioniert teilweise | 09.04.2016 |
| SeriesEver     | seriesever.net    | funktioniert           | 09.04.2016 |
| StreamIt       | streamit.ws       | funktioniert           | 19.09.2016 |
| StreamKisteTV    | streamkiste.tv    | funktioniert           | 27.10.2016 |
| SzeneStreams   | szene-streams.com | funktioniert           | 09.04.2016 |
| Tata           | tata.to           | funktioniert           | 17.09.2016 |
| Video2k        | video2k.is        | funktioniert           | 28.09.2016 |
| Video4k        | video4k.to        | funktioniert           | 20.09.2016 |

Empfehlungen und Vorschläge für neue Seiten können über das [Forum](http://xstream-addon.square7.ch) unter dem Bereich [Wünsche und Anregungen](http://xstream-addon.square7.ch/forumdisplay.php?fid=9) angefragt bzw. eingestellt werden. Die Intergration der eingereichten Seiten ist nicht selbsverständlich und folgt daraufhin nicht automatisch. Sowohl das Potenzial der vorgeschlagenen Seite als auch der erforderliche Mehrwert wird geprüft und entscheidet über die Entwicklung eines neuen Site-Plugins.
Grundsätzlich ist jedoch zu erwähnen, dass stätig an der weiterentwicklung von xStream und deren Site-Plugins gearbeitet wird.


### 1.2 Rechtliche Konsequenzen bei Nutzung

Nein, das Addon ermöglicht nur die Nutzung der Streaming-Seiten. Das bloße Streamen hat in Deutschland (momentan) keine rechtlichen Konsequenzen. Die meisten Streaming-Seiten speichern keine Zugriffsdaten. Hier ist ein Video von Rechtsanwalt Christian Solmecke, der über das Thema rechtlich aufklärt:

[![Nutzerfragen: Legalität von Streaming, Arbeitszeiten und Bild.de | Rechtsanwalt Christian Solmecke](http://img.youtube.com/vi/cDmvhJrLkmM/0.jpg)](http://www.youtube.com/watch?v=cDmvhJrLkmM)



## 2. Installation und Konfiguration


### 2.1 Bezugsquellen zur Installation

Das Plugin kann direkt herunterladen werden (wobei die Update-Funktionalität nicht gegeben ist), oder über die xStream Repository installiert werden (empfohlen). Diese ist momentan hier verfügbar:

***WICHTIG:*** Beim gesamten Daten Download von Github gilt es folgendes zu Beachten: 
Um eine Korrekte Installation zu Gewährleisten, ist es immer notwendig, den Anhang _Master, Beta, Nightly_ aus den  .zip Dateien und dem Unterordner zu entfernen

Geht wie folgt: 
	
- zum Beispiel, die Datei in "plugin.video.xstream.zip" umbenennen (quasi das "-master", -"beta" oder -"nightly" entfernen)

-  Datei öffnen (nicht entpacken) mit 7-Zip, WinRAR, WinZIP (oder einem anderen Packer)
	
- dort ist ein Ordner zu sehen der z.B. "plugin.video.xstream-master" heißt => auch hier das "-master" entfernen

Die Zip dann installieren.

xStream-Repository aus dem Forum:

- [xStream-Forum](http://xstream-addon.square7.ch/showthread.php?tid=1)

- [Master-Branch bei GitHub](https://github.com/Lynx187/xStreamRepo/archive/master.zip)

Alternativer Download der Repository:

- [SuperRepo](https://superrepo.org/kodi/addon/repository.xstream/)
***WICHTIG:*** Jedoch muss an dieser Stelle klar darauf hingewiesen werden, dass unter der alternativen Bezugsquelle nicht für den aktuellsten Stand und Funktion der Software garantiert werden kann!

Zusätzlich kann man auch die neuste Version von xStream benutzen, indem man die Nightly bzw. Beta Version herunterlädt.

- [Beta-Branch bei GitHub](https://github.com/StoneOffStones/plugin.video.xstream/tree/beta)
- [Nightly-Branch bei GitHub](https://github.com/xStream-Kodi/plugin.video.xstream/tree/nightly)

**ACHTUNG!** *Die Beta und Nightly Versionen gelten als Experimentell und werden nicht offiziell unterstützt.*

Nach dem das Repo Installiert wurde ist noch folgendes zu machen:

- öffnet die Kategorie Addons
- Aus Repository installieren
- xStream Repository
- *Video-Addons*
- xStream (installieren/aktivieren)
- *Addon Verzeichnis*
  hier TVADDONS.ag Libraries Repository aktivieren
  (dann wird der URL-Resolver automatisch aktualisiert)

Im Anschluss kann dann das xStream „Autoupdate“ gemacht werden (muss aber nicht), wie unten Beschrieben
Hier empfehle ich „nightly“ zu nehmen 


### 2.2 Allgemeine Einstellungen

Unter der Auswahl der jeweiligen Sprache kann die jeweilig bevorzugte Sprache ausgewählt werden. Dabei kann unter den Optionen Deutsch, Englisch und Alle gewählt werden, wobei Alle beide Sprachen einbezieht. Zu berücksichtigen ist jedoch, dass die einzelnen Site-Plugins diese Option unterstützen müssen. Wird also die aufgezählte Option nicht unterstützt werden auch Inhalte anderer Sprache angezeigt. Sonst am besten alles so lassen wie es ist, die Views leer lassen, sowie die Downloads.

Wenn gesehene Filme auf einmal weg sind, liegt das an den Einstellungen im Seitenmenü. Hier die Markierung „gesehene Filme“ deaktivieren!

Seit xStream 2.2.0 und in den Nightly/Beta Versionen, gibt es in den Settings eine:

 **Auto-Update Funktion**. 
Diese installiert automatisch Änderungen *an Seiten* usw., welche auf der Entwicklerplattform (Github) durchgeführt werden.
Das Updatet nimmt die aktuelle nighly Version

**UrlResolver Auto-Update**
Diese installiert automatisch Änderungen des *URL Resolvers* (tknorris) usw., welche auf der Entwicklerplattform (Github) durchgeführt werden.

Dadurch werden Fehler/Bugs/Error, schnell & einfach behoben. 

Als Standard ist bei beiden aktiviert eingestellt.
Nightly ist eine Entwicklerversion, Fehler können da natürlich auftreten
Die nightly ist aber am  aktuellsten

Diese Auto-Updates werden nur ausgeführt, wenn es aktiviert ist und man das xStream Addon öffnet:
*Desktop- Videos -Addons- Video Addons- xStream*
*Kodi17: Desktop- Addons- xStream*

Diese xStream Auto-Update Funktion arbeitet Unabhängig von den KODI Einstellungen. 

Wenn in Kodi unter: Optionen-Einstellungen-Addons- Seitenmenü, Automatische Aktualisierung auf AUS gestellt ist wird xStream trotzdem aktualisiert

### 2.3 Webseiten Aktivieren und Deaktivieren

*Standard:* Alle Site-Plugins aktiviert

In den Einstellungen, unter dem Menüpunkt *Site-Plugins*, besteht die Möglichkeit bestimmte Seiten an bzw. auszuschalten. 
Dies kann von Nutzen sein, wenn kein Interesse an bestimmten Medien besteht. 
Diese werden dann auch nicht in der globalen Suche angezeigt.

Hier **muß** mindesten eine Seite ausgewählt werden, sonst kann das Fenster nicht geschlossen werden!!

Nache einem Update werden auch neu hinzugefügte Seiten automatisch angezeigt

### 2.4 Manuelle und automatische Hosterwahl

Die Hosterwahl als solches ist sehr schlicht und einfach gehalten. Es erinnert stark an die eigentlichen Benuteroberflächen der jeweiligen Streaming-Seiten

Wenn keine besonderen Wünsche bzw. keine entprechende Kenntisse im Bezug auf die Hosterauswahl vorhanden sind, kann die Automatische Hosterwahl verwendet werden. In dieser Einstellung werden darüber hinaus nicht funktionierende Hoster rausgefiltert. 

**Hosterauswahl**

*Dialog*
Bei Aktivierung wird die Hosterauswahl als Pop-Up Fenster dargestellt

*Hosterliste*
Bei Aktivierung wird die Hosterauswahl nicht mehr als Pop-Up-Fenster dargestellt, sondern als normale Verzeichnisliste.

*Auto*
Automatische Hosterauswahl

**Hosterliste prüfen und sortieren**

Bei Aktivierung werden aus der Hosterliste alle nicht unterstützten Hoster entfernt und nach ihrer Priorität (Resolver Settings) sortiert.
Diese kann unter "Resolver Settings" angepasst werden. 

*Niedrige Werte werden vor hohen Werten gewählt*

Die Deaktivierung diese Features kann auf leistungsschwachen System (z.B. RPi) einen spürbar schnelleren Ablauf bewirken.

Ich würde die Deaktivierung Empfehlen, da es nicht wirklich notwendig ist (und manchmal für Fehler verantwortlich ist)

***Anmerkung zu dem Hoster Openload (HD):***
Wenn Ihr diesen Hoster zum Streamen auswählt, erscheint ein Fenster, welches Euch auffordert Eure Gerät zu Pairen.
Das könnt ihr mit ruhigen Gewissen machen, wie?

Ihr müsst im selben WLAN sein wie das zu Pairende Gerät (z.B. FireTV, Apple TV usw.)
Öffnet am Handy/Tablet/PC einen Browser mit der angezeigten Adresse von openload (https://openload.co/pair)
Klickt in dem Kasten bei “Ich bin kein Roboter”
Dann ganz runter und klick auf “Pair”
Das wars.
Dieser Vorgang muss immer wieder Wiederholt werden (nach 4 Stunden oder 5 Streams)

### 2.5 Metahandler benutzen

Bei Aktivierung wird das externe Modul metahandler genutzt um ausführliche Informationen in Form von Metadaten, wie Fanarts, Covers oder Episodenbilder, zu den Streams bereitzustellen.
Ermöglicht eine relativ konsistente Verwendung der "gesehen" Markierung.
Bei erstmaliger Verwendung dauern die Ladevorgänge deutlich länger. Dies liegt daran, dass  zunächst alle neuen Informationen zusätzlich über das Internet abgerufen werden müssen.
Für schwache Systeme nur bedingt zu empfehlen.
Muss vom jeweiligen Site-Plugin unterstützt werden, sonst zeigt diese Option keine Funktion.

- **Metahandler ersetzt Infos von Site**

- Bei Aktivierung werden Metainformationen vom  "Metahandler" bevorzugt. D.h. Metainformationen die von einem Site-Plugin geliefert wurden werden nicht nur ergänzt sondern auch ersetzt.

- ***ACHTUNG:*** Da viele Seiten nicht sofort genug Informationen bereitstellen um jeden Film eindeutig zu identifizieren kann es vorkommen, dass alle angezeigten Informationen nicht zum tatsächlich verlinkten Film passen.

### 2.6 Autoplay Funktion

Ist diese Option aktiviert, wird keine Hosterliste angezeigt. 
xStream probiert automatisch alle verfügbaren Hoster aus, bis ein Stream abgespielt werden kann. 
Die Auswahlreihenfolge der Hoster richtet sich nach deren Priorität. Diese kann unter "Resolver Settings" angepasst werden. 
*Niedrige Werte werden vor hohen Werten gewählt*

Bevorzugte Qualität bei Auto-Play: 
hier kann die Qualität der Streams eingestellt werden
Ist Best eingestellt,  wir immer der beste verfügbare Stream gewählt

### 2.7 Zentralisierte Einstellungen
Wenn AUS: werden im Hauptmenü 3 Ordner (Globale Suche, xStream Einstellungen, Resolver Einstellungen) angezeigt

Wenn EIN: wird nur Globale Suche & Einstellungen angezeigt.
Einstellungen beinhaltet (xStream Einstellungen & Resolver Einstellungen)

## 3. Bekannte Probleme


### 3.1 Fehler bei der Installation

Fehler können verschiedene Ursachen haben. Bei Hilfe bitte immer folgendes bekannt geben:
Log, Kodi Version, Betriebssystem, xStream Version, genaue Fehlerbeschreibung!

Wird die 2.1.16 Beta installiert, ist es vorher notwendig das script.modul Cryptopy  zu installieren  und vor dem Entpacken den Zusatz -master aus der .zip entfernen:

- https://github.com/StoneOffStones/script.module.cryptopy/archive/master.zip

Bitte, schauen, ob der Fehler in einem früheren Post schon beantwortet wurde!
Es kann auch eine fehlerhafte Datei vorliegen, oder die .zip ist falsch aufbereitet.


### 3.2 Fehler bei Verwendung der Globalen Suche

Falls bei der Globalen Suche eine Fehlermeldung bekommen, dass eine Seite nicht erreichbar war bzw. die Suche durch eine Meldung unterbrochen wurde, liegt dies meist an der Seite. Meistens sind die Seiten in diesem Moment nicht erreichbar, einfach abwarten.
Es kann auch vorkommen, dass bei der Globalen Suche keine Treffer angezeigt werden, dann bitte in der gewünschten Seite die Suche nutzen (manchmal stören die Seiten, die Globale Suche).  
Um schnelle Abhilfe zu leisten lohnt es sich in diesem Fall durchaus die Entwicklergemeinde darauf aufmerksam zu machen

### 3.3 Fehler bei Verwendung einzelner Webseiten

Das kann verschiedene Ursachen haben. Meistens liegt es jedoch an der eigentlichen Webseite.
Denn wenn dort auch nur eine Kleinigkeit geändert wird, kann es schon sein, dass  das Site-Plugin nicht mehr geht.
Die Entwickler wissen es meist und arbeiten an einer Lösung. Bitte Sachlich bleiben und nicht jammern!
Die Seite im Browser aufrufen und auf Funktion überprüfen.
Im Anschluss das Problem schildern.

*Für die Streaming-Seiten kinox.to und movie4k.to können in den Einstellungen alternative Domäne bestimmt werden. Nutzen sie diese falls die Seiten nicht zu erreichen sind!*

### 3.4 URL Resolver Fehler

Sollte dies der Fall sein, bitte den aktuellste Version des "URLResolver" über eine der folgenden Bezugsquellen beziehen:

- URLResolver über die TVA Repo laden welches Bestandteil der offiziellen xStream-Repo ist

- https://offshoregit.com/tvaresolvers/tva-common-repository/raw/master/zips/script.module.urlresolver/

- Alternativ kann man den neusten URL Resolver auch von hier beziehen:

 https://github.com/tknorris/script.module.urlresolver/archive/master.zip

Bitte den gewünschten Film auf der Homepage auf Funktion kontrollieren.

**Ein Hoster (z.B. flashx) geht bei allen nur bei Euch nicht**

Das kann an einer falschen Installation des URL Resolver liegen 
(z.B. das - master wurde nicht entfernt bei Downloads von Github vor der Installation oder URL Resolver ist 2 mal vorhanden usw.)

*Wenn dieser Fehler auftreten sollte, kann folgendes helfen:*

Alle Ordner, die zum URLResolver gehören, löschen. 

Und zwar einmal im ..kodi/addons-Ordner, script.modul.urlsresolver löschen und zum anderen im ...kodi/userdata/addon_data-Ordner, script.modul.urlsresolver -löschen

Dann installierst du den aktuellsten URL Resolver aus der [.zip von tknorris bei Github](https://github.com/tknorris/script.module.urlresolver/archive/master.zip)

### 3.5 Fehlermeldungen im Betrieb

- **ImportError:** Bad magic number in bs_finalizer.pyo

	- Status: Problem behoben (Master)

	- Thread: [Link](http://xstream-addon.square7.ch/showthread.php?tid=505)

- **TypeError:** string indices must be integers

	- Status: Problem behoben (Master)

	- Thread: [Link](http://xstream-addon.square7.ch/showthread.php?tid=608)

- **AttributeError:** "...Resolver" object has no attribute "priority"

	- Status: Problem behoben (Master)

	- Thread: [Link](http://xstream-addon.square7.ch/showthread.php?tid=604)

- **KeyError:**'TVShowTitle'

	- Status: Problem behoben (Master)

- **Movie4k funktioniert nicht**

	- Status: Problem behoben (Beta)

	- Thread: [Link](http://xstream-addon.square7.ch/showthread.php?tid=610)

- **Metahandler funktioniert nicht**

	- Status: Problem bekannt, ist in Arbeit

Angaben in (...) = Aktueller "Ort"

- Master  =>  Ist im aktuellen Master Branch, fix kommt in der nächsten Version

- Beta    =>  Ist im Beta Branch  [(siehe: xStream Beta/Nightly)](http://xstream-addon.square7.ch/showthread.php?tid=584)
- Nightly =>  Ist im Nightly Branch [(siehe: xStream Beta/Nightly)](http://xstream-addon.square7.ch/showthread.php?tid=584)

- **Beim Starten von Xstream kommt folgende Fehlermeldung**

	- "IOError: [Errno socket error] [SSL:
CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:590)
	
	- Status: Problem behoben (Master)

	- *Anmerkung:* in den xStream-Settings die Suche nach Updates ausschalten, dann läuft es wieder
Updates von Git muss man dann manuell einspielen oder auf Updates über das offizielle xStreamRepo warten

	- Thread: [Link](http://xstream-addon.square7.ch/showthread.php?tid=618)

- **Beim öffenen von Serien/Filmen in xStream kommt folgende Fehlermeldung**

	- AttributeError:´loadError´ object has no attribute ´encode´
	
	- Lösung: 
	Kodi (und daher auch xStream) mag keine Sonderzeichen im Benutzernamen
Sonderzeichen im Benutzernamen entfernen dann geht es

- **Fehler 1 beim Öffnen von BurningSeries (Bs)**
	- [SSL:CERTIFICATE_VERIFY_FAILED] certificate failed (sl.c:590)

		und danach kommt eine Fehlermeldung:

		ValueError MO JSON object could be decoded File 
"/Users/Shared/xbmc-depends/appletvos9.1_arm64-target/lib 
line 366, in decode
	- Status: Problem behoben (Master)

 - Thread: [Link](http://xstream-addon.square7.ch/showthread.php?tid=627)
 
- **Fehler 2 beim Öffnen von BurningSeries (Bs):** 
  - ImportError: No Module named t0mm0. Common.net /script. Module. Urlresolver /lib/urlresolver /plugins /ecostrean. Pline 19,in < module> 

	- Lösung: Es fehlt eine Abhängigkeit von xStream, welche eigentlich bei der Installation über das Repo mit installiert werden sollte.
Deinstalliert xStream nochmal und installier es über das xStream Repo neu (oder von Git die [master](https://github.com/StoneOffStones/plugin.video.xstream/archive/master.zip))

	- Thread: [Link](http://xstream-addon.square7.ch/showthread.php?tid=627&page=2)

- **Fehlermeldung beim öffnen eines Sit-Plugin**
 - Errno4 non-recoverable failure in the name  Resolution.Fehler
	
		Weist auf ein Problem bei der Namesauflösung der Domains hin. Könnte z.B. an der eingestellten DNS liegen (oder VPN) oder aber auch an den netzwerkbezogenen Einstellungen von Kodi

	- Lösung: Database im Profilordner von xStream löschen, wie folgt:
 Optionen-Dateimanager-Profil_Ordner-addon_data-plugin.Video.xstream-pluginDB wählen und löschen
	- Thread: [Link](http://xstream-addon.square7.ch/showthread.php?tid=516)
		
- **Anzeige: Es ist mehr als ein URLResolver installiert. Bitte löschen**

	Das Problem entsteht durch komische Repos oder durch manuelle Installation (wenn man beim Installieren in der .zip nicht das "-master" entfernt)
Dadurch wird dann ein zweiter URLResolver angelegt und das führt dann zum Problem.

	- Lösung:  geht im Kodi Ordner zu ..../kodi/addons/
	Dort werdet ihr dann Ordner finden die mit wie folgt heißen:

	    - script.module.urlresolver
	    - script.module.urlresolver-master


	Einfach den Ordner mit "-master" am Ende löschen und die Fehlermeldung ist weg. Und auch das AutoUpdate im xStream funktioniert wieder.
xStream verwendet KEINEN eigenen URLResolver. Wird benutzen den der im System installierten.	
			
- Thread: [Link](http://xstream-addon.square7.ch/showthread.php?tid=808&pid=5928#pid5928)
		
- **Errno 1 bzw. Errno 8 Fehlermeldung bei Seiten**

	Die Webseitenbetreiber & Hoster stellen Ihre  Verschlüsselung um.
Das Problem hat nichts mit xStream zu tun. 
Es liegt an Kodi, bzw. der Pythonversion welche Kodi verwendet. 
Ist diese veraltet (Kodi 16.1 abwärts) kommte es zur Fehlermeldung bei diversen Site-Plugins / Hoster.

	- Lösung: Kodi 17 verwenden

	- Thread: [Link](http://xstream-addon.square7.ch/showthread.php?tid=814)

## 4. Fehlerbericht über Log-Datei


### 4.1. Allgemeines zur Log-Datei

In dem log File werden alle Aktivitäten/Programmabläufe von Kodi protokolliert und gespeichert. Wenn man nun Probleme mit Kodi hat, ist es sehr hilfreich, dieses Log File im Forum zu Posten. Nur so kann eine schnelle und Zielgerichtete Lösung erfolgen.


### 4.2 Speicherort der Log Datei

Den Speicherpfad von Kodi anzeigen lassen – Scroll weiter runter zum Punk Debug_Loggin und folgen den Beschreibungen.

Das ist immer vom Betriebssystem abhängig.
Im Folgenden werden bekannte Ordnerstrukturen der jeweiligen Betriebssysteme aufgelistet. Anstelle von "xbmc" kann in den Ordnern auch "kodi" stehen
(die Ordnerstruktur kann jedoch auch leicht von dieser Anleitung abweichen):

- Windows XP
    - `Documents and Settings\<your_user_name>\Application Data\Kodi`
- Vista/Windows 7
    - `C:\Users\<your_user_name>/%APPDATA%/Roaming/Kodi/Kodi.log`
- Mac OS X
    - `/Users/<username>/Library/Logs/ oder`
    - `/Users/<your_user_name>/Library/Application Support/Kodi/userdata`
- iOS
    - `/private/var/mobile/Library/Preferences`
- Linux, OpenElec, Raspberry Pi 1-3
    - `$HOME/.kodi/temp/`
    - `$HOME/.kodi/userdata/temp/xbmc.log`
    - `$HOME/.kodi/userdata`
- Android
    - `/android/data/org.xbmc.Kodi/files/.kodi/temp`
    - `data/data/org.xbmc.Kodi/cache/temp`

Die Ordner sind meist versteckt und müssen sichtbar gemacht werden, im Windows Explorer oder auf Android mit dem ESDateiexplorer.

Das Log File kann am besten mit Notepad++  unter Windows oder gedit unter Linux betrachtet werden.
Auch der normale Texteditor unter Windows geht, Notepad ist aber übersichtlicher.
Auf Android einen Texteditor verwenden zum Betrachten.
Übrigens die Kodi „log.old“ ist die Logdatei vom letzten Neustart/Crash. Also wenn man keine mehr erstellen kann, dann diese nehmen.


### 4.3. Erstellen und Hochladen der Log-Datei

Kodi hat Standardmäßig die beiden wichtigen Log Addons integriert (eines zum Lesen der Log, das andere zum Hochladen). Damit ist das Erstellen der Log Datei und Posten im Forum sehr viel einfacher.

In Kodi gehe zu:

- Desktop-Optionen
- Einstellungen
- Addons
- Suche

In die Zeile "log" ein und Klicks auf Fertig.

Folgende Addons auswählen und installieren diese:

Log Viewer für Kodi (nur zum Lesen der Log-Datei)
Kodi Log Uploader (zum Auslesen & Uploaden der Log-Datei)

Mit dem LogViewer kann man die Log Datei ansehen, mit dem LogUploaded das Log-File auf http://xbmclogs.com hochladen.

Bei der Installation eine E-Mail Adresse angeben. An diese wird dir dann nach dem LogUpload ein Link zur Log Datei geschickt.
Diesen Link im Forum Posten oder alles in einen Texteditor koperien, Die Datei speicherun und im Forum hochladen.

Debug-Logging (Kodi GUI):

Manchmal ist es gut das Debug Logging in Kodi zu aktivieren um noch mehr Informationen zu erhalten.

Folgendes Ausführen:
 Desktop-Optionen
 
- Einstellungen
- System
- Debugging
- "Debug-Logging aktivieren" anklicken

Fertig

Es wird nun am oberen Rand eine Statuszeile eingeblendet mit Infos; **Hier ist auch der Speicherort der Log-Datei zu sehen!**

Starte Kodi neu und öffne das Addon welches einen Fehler verursacht. Erstellen dann sofort eine Log-Datei (dann ist der Fehler leichter herauszulesen).

Das Debug-Logging kann im Anschluss wieder deaktiviert werden.

Unter dem Punkt  Komponentenspezifische Protokollierung kann man bei der Kategorie "Konfiguration der Komponentenspezifischen Protokollierung" noch Einstellen was alles im Debug-Log Protokolliert werden soll.


## 5. Phyton Dateien


### 5.1. Allgemeines zur .py-Datei

Eine .py Datei ist eigentlich eine Textdatei. Die Endung .py verweist auf die Programmiersprache Python, welche in Kodi zur Anwendung kommt.Diese .py Dateien werden in sämtlichen/den meisten Addons verwendet.
 
 
### 5.2 Bearbeiten einer .py-Datei

Manchmal werdet Ihr lesen z.B. Wechsel die .py Datei in dem Ordner „xyz“, oder ändere den Eintrag in Zeile 134.Öffnen könnt Ihr die Datei mit vielen Programmen z.B. Notepad++ (Freeware) oder Texteditor. In Notepad werden Euch die Zeilen-Nummern angezeigt und ist somit übersichtlicher, aber es geht auch mit dem EditorMit Notepad++ könnt Ihr die .py Datei sofort öffnen und wieder speichern.

Bei Verwendung des Text-Editors müsst Ihr die Endung vorher von .py auf .txt ändern. Dann könnt Ihr die Datei öffnen und Änderungen vornehmen. Im Anschluss bitte „Speichern unter“ wählen und bei „Dateityp“ alle wählen, und wieder als .py Datei speichern


### 5.3 Speicherort der einzelnen Webseiten (.py Dateien)

In den folgenden Ordnern findet Ihr alle Addons von Kodi. Das Addon xStream wird in aller Regel unter plugin.video.xstream istalliert.

- Android 
	- `/Android/data/org.xbmc.kodi/files/.kodi/addons/`
	- `/sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/`  (.kodi ist ein versteckter Ordner)
- iOS
	- `/private/var/mobile/Library/Preferences/Kodi/addons/`
- Linux 
	- `~/.kodi/addons/`
- Mac 
	- `/Users/<your_user_name>/Library/Application Support/Kodi/addons/`
- OpenELEC 
	- `/storage/.kodi/addons/`
- Windows
	- `C:\Users\BENUTZERNAME\AppData\Roaming\Kodi\addons`    (AppData ist ein versteckter Ordner)

Das Addon xStream wird in aller Regel unter plugin.video.xstream istalliert.

Im Verzeichnis `sites/` sind die .py Daten und im Ordner `resources/art/sites/` die jeweiligen Artworks bzw. Site-Icons der einzelnen Webseiten abgelegt.

