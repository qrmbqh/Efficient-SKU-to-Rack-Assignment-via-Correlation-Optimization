function [sku2, targetrack, bestchange] = algorithm5(A,B,C,sourcerack,sku,bestchange)
for rack = 1:size(B,2)
    if rack ~= sourcerack
        change = algorithm4(A, B, C, sourcerack, rack, sku);
        if change < bestchange
            bestchange = change;
            sku2 = sku;
            targetrack = rack;
        end
    end
end