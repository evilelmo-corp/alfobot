def profe_mode():
  await ctx.send('Chicos vamos serios, hablen')
  @client.event
  async def on_message(message):
    if message.author != client.user:
      if "duerme" in message.content:
        await client.logout()
      if message.content in list(df_data.key):
        await message.channel.send(df_data[df_data['key']==str(message.content)]["value"])