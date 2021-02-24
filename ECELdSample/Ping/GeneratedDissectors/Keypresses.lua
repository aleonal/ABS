-- Keypresses frame number-based postdissector
-- declare Fields to be read
-- declare our (pseudo) protocol
Keypresses_proto = Proto("keypresses","Keypresses Log")
-- create the fields for our "protocol"
timestamp_F = ProtoField.string("keypresses.timestamp","Original Event Timestamp")
eventdata_F = ProtoField.string("keypresses.data","Log Data")

-- add the field to the protocol
Keypresses_proto.fields = {timestamp_F, eventdata_F}

-- create a function to "postdissect" each frame
function Keypresses_proto.dissector(buffer,pinfo,tree)
    -- add the data based on timestamps
    if pinfo.abs_ts >= 1613199476.0 and pinfo.abs_ts <= 1613199478.0 then
       local subtree = tree:add(Keypresses_proto,"Keypresses Log")
       local mycomplientstr = tostring("ping 8.8.8.8")

       subtree:add(timestamp_F,tostring("2021-02-13T06:57:56"))
       subtree:add(eventdata_F, mycomplientstr)
    end
end
-- register our protocol as a postdissector
register_postdissector(Keypresses_proto)