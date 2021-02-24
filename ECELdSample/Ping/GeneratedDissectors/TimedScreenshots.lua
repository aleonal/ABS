-- TimedScreenshots frame number-based postdissector
-- declare Fields to be read
-- declare our (pseudo) protocol
TimedScreenshots_proto = Proto("timedscreenshots","TimedScreenshots Log")
-- create the fields for our "protocol"
timestamp_F = ProtoField.string("timedscreenshots.timestamp","Original Event Timestamp")
eventdata_F = ProtoField.string("timedscreenshots.data","Log Data")

-- add the field to the protocol
TimedScreenshots_proto.fields = {timestamp_F, eventdata_F}

-- create a function to "postdissect" each frame
function TimedScreenshots_proto.dissector(buffer,pinfo,tree)
    -- add the data based on timestamps
    if pinfo.abs_ts >= 1613199491.0 and pinfo.abs_ts <= 1613199493.0 then
       local subtree = tree:add(TimedScreenshots_proto,"TimedScreenshots Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/timed_screenshots/1613199491.519802_screenshot.png")

       subtree:add(timestamp_F,tostring("2021-02-13T06:58:11"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1613199457.0 and pinfo.abs_ts <= 1613199459.0 then
       local subtree = tree:add(TimedScreenshots_proto,"TimedScreenshots Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/timed_screenshots/1613199457.166161_screenshot.png")

       subtree:add(timestamp_F,tostring("2021-02-13T06:57:37"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1613199553.0 and pinfo.abs_ts <= 1613199555.0 then
       local subtree = tree:add(TimedScreenshots_proto,"TimedScreenshots Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/timed_screenshots/1613199553.153683_screenshot.png")

       subtree:add(timestamp_F,tostring("2021-02-13T06:59:13"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1613199468.0 and pinfo.abs_ts <= 1613199470.0 then
       local subtree = tree:add(TimedScreenshots_proto,"TimedScreenshots Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/timed_screenshots/1613199468.4591508_screenshot.png")

       subtree:add(timestamp_F,tostring("2021-02-13T06:57:48"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1613199479.0 and pinfo.abs_ts <= 1613199481.0 then
       local subtree = tree:add(TimedScreenshots_proto,"TimedScreenshots Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/timed_screenshots/1613199479.8863199_screenshot.png")

       subtree:add(timestamp_F,tostring("2021-02-13T06:57:59"))
       subtree:add(eventdata_F, mycomplientstr)
    end
end
-- register our protocol as a postdissector
register_postdissector(TimedScreenshots_proto)