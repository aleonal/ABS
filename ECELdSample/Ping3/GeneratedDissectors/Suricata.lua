-- Suricata frame number-based postdissector
-- declare Fields to be read
-- declare our (pseudo) protocol
Suricata_proto = Proto("suricata","Suricata Log")
-- create the fields for our "protocol"
timestamp_F = ProtoField.string("suricata.timestamp","Original Event Timestamp")
eventdata_F = ProtoField.string("suricata.data","Log Data")

-- add the field to the protocol
Suricata_proto.fields = {timestamp_F, eventdata_F}

-- create a function to "postdissect" each frame
function Suricata_proto.dissector(buffer,pinfo,tree)
    -- add the data based on timestamps
    if pinfo.abs_ts >= 1614328597.0 and pinfo.abs_ts <= 1614328599.0 then
       local subtree = tree:add(Suricata_proto,"Suricata Log")
       local mycomplientstr = tostring("PING ")

       subtree:add(timestamp_F,tostring("2021-02-26T08:36:37"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1614328597.0 and pinfo.abs_ts <= 1614328599.0 then
       local subtree = tree:add(Suricata_proto,"Suricata Log")
       local mycomplientstr = tostring("PING ")

       subtree:add(timestamp_F,tostring("2021-02-26T08:36:37"))
       subtree:add(eventdata_F, mycomplientstr)
    end
end
-- register our protocol as a postdissector
register_postdissector(Suricata_proto)