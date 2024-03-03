## POEM_OS

Read the [backoffice blog post here](https://backoffice.nearfuturelaboratory.com/blog/2024/03/poem-os-a-contribution-to-the-poem-vibe/)

This knits together a poem project from 2004 with OpenAI, ElevenLabs and Design Fiction.

You'll need OpenAI and ElevenLabs API keys. You'll also need the ids of the voices you have access to from your ElevenLabs account.

Those go into a file called config.json that should look simply like this:

```
{
"api_keys": {
      "openai": "XXXXX",
      "elevenlabs": "YYYYY"
    },
  "data_root": "../" 
}

```

`data_root` is the directory relative to this one in which you want to store the outputs which will go into directories named according to the day of the week you ran `poem_os_01.py`. In those directories will be date & time named files, including a JSON file that is effectively a log of what was done and the poem, and a .mp3 file that is the reading of the Poem.

```
{
    "day": "sunday",
    "prompt": "Write a short pithy sonnet about Sunday in anticipation of Monday. Keep it short so that it can be read in under 30 seconds.",
    "poem": "In Sunday's gentle grasp, we softly lie,\nA tender pause 'fore Monday's stern decree,\nIn golden beams and azure painted sky,\nA fleeting haven in time's boundless sea.\n\nYet in each silent whisper, shadows loom,\nOf tasks delayed and hours yet to spend,\nA prelude to the coming day's resume,\nWhere hopes are set and dreams dare to extend.\n\nBut let not sorrow for the morrow's strife,\nEclipse the joy in restful moments gained,\nFor every Sunday holds the gift of life,\nA chance to breathe before the week's reclaimed.\n\nEmbrace the calm, let peace your heart bestow,\nFor in this rest, the strength for Monday grows.",
    "voice_name": "Natasha - Valley girl",
    "voice_id": "M50LFkrW6e1TVKSwGEt1",
    "date": "03032024",
    "audio": {
        "filename": "sunday_03032024_125800_0.mp3",
        "duration": 34.351,
        "timed_filename": "sunday_03032024_125800_0"
    }
}
```
