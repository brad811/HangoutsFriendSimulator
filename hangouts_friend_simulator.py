import json
import markovify
import sys

if len(sys.argv) < 2:
  print("usage: hangouts_friend_simulator.py input_file [person ...]")
  sys.exit(1)

input_filename = sys.argv[1]

people_whitelist = []

for person in sys.argv[2:]:
  people_whitelist.append(person)

people_data = {}

try:
  with open(input_filename) as json_data:
    data = json.load(json_data)
except FileNotFoundError:
  print("Could not find input file: " + input_filename)
  sys.exit(1)

for conv_container in data["conversation_state"]:
  conversation_state = conv_container["conversation_state"]
  conversation = conversation_state["conversation"]

  participants = conversation["participant_data"]
  for participant in participants:
    try:
      chat_id = participant["id"]["chat_id"]
      if chat_id not in people_data:
        #print("Adding participant: " + participant["fallback_name"])
        people_data[chat_id] = {}
        people_data[chat_id]["name"] = participant["fallback_name"]
        people_data[chat_id]["messages"] = []
    except KeyError:
      pass

  events = conversation_state["event"]
  for event in events:
    sender_id = event["sender_id"]["chat_id"]

    if sender_id not in people_data:
      continue

    if "messages" not in people_data[sender_id]:
      continue

    if "chat_message" not in event:
      continue

    if "segment" not in event["chat_message"]["message_content"]:
      continue

    segments = event["chat_message"]["message_content"]["segment"]

    message = ""

    for segment in segments:
      if "text" not in segment.keys():
        # some segments don't have text, like: {'type': 'LINE_BREAK'}
        continue
      message += segment["text"]

    people_data[sender_id]["messages"].append(message)

for person_id in people_data:
  person = people_data[person_id]

  if "name" not in person:
    continue

  if len(people_whitelist) > 0 and person["name"] not in people_whitelist:
    continue

  try:
    text_model = markovify.NewlineText( "\n".join(person["messages"]), state_size=3 )
  except IndexError:
    # markovify didn't like the input messages
    pass

  sentence = text_model.make_sentence(tries=1000, max_overlap_ration=0.5, max_overlap_total=10)
  if sentence == None:
    continue

  print("----------")
  print(person["name"] + ":")
  print(sentence)

print("----------")
